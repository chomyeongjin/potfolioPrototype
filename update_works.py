import re

with open('works.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HTML dropdown
html = re.sub(
    r'<div class="filter-group tag-filters dropdown-group">.*?</div>\s*</div>',
    """<div class="filter-group tag-filters dropdown-group">
                <button class="dropdown-toggle" aria-expanded="false">Tag: All <span>&#9662;</span></button>
                <div class="dropdown-content">
                    <button class="filter-btn active" data-type="tag" data-filter="all">All</button>
                </div>
            </div>""",
    html,
    flags=re.DOTALL
)

# 2. Extract script replacement
new_script = """        const gridItems = document.querySelectorAll('.grid-item');
        let activeLocation = 'all';
        let activeTags = new Set(['all']);

        function attachFilterLogic(btn) {
            btn.addEventListener('click', () => {
                const type = btn.getAttribute('data-type');
                const filterValue = btn.getAttribute('data-filter');
                const dropdownToggle = btn.closest('.dropdown-group').querySelector('.dropdown-toggle');

                if (type === 'location') {
                    document.querySelectorAll(`.filter-btn[data-type="location"]`).forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    activeLocation = filterValue;

                    const displayValue = filterValue === 'all' ? 'All' : btn.textContent;
                    dropdownToggle.innerHTML = `Place: ${displayValue} <span>&#9662;</span>`;

                    dropdownToggle.classList.remove('active');
                    dropdownToggle.nextElementSibling.classList.remove('active');
                    dropdownToggle.setAttribute('aria-expanded', 'false');
                } else if (type === 'tag') {
                    if (filterValue === 'all') {
                        activeTags.clear();
                        activeTags.add('all');
                        document.querySelectorAll(`.filter-btn[data-type="tag"]`).forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                    } else {
                        activeTags.delete('all');
                        const allBtn = document.querySelector(`.filter-btn[data-type="tag"][data-filter="all"]`);
                        if (allBtn) allBtn.classList.remove('active');

                        if (activeTags.has(filterValue)) {
                            activeTags.delete(filterValue);
                            btn.classList.remove('active');
                        } else {
                            activeTags.add(filterValue);
                            btn.classList.add('active');
                        }

                        if (activeTags.size === 0) {
                            activeTags.add('all');
                            if (allBtn) allBtn.classList.add('active');
                        }
                    }

                    let displayValue = 'All';
                    if (!activeTags.has('all')) {
                        const activeBtns = Array.from(document.querySelectorAll(`.filter-btn[data-type="tag"].active`));
                        if (activeBtns.length <= 2) {
                            displayValue = activeBtns.map(b => b.textContent).join(', ');
                        } else {
                            displayValue = `${activeBtns.length} selected`;
                        }
                    }
                    dropdownToggle.innerHTML = `Tag: ${displayValue} <span>&#9662;</span>`;
                }

                // Filter the grid items
                gridItems.forEach(item => {
                    const itemLocation = item.getAttribute('data-location');
                    const itemTag = item.getAttribute('data-tag');

                    const locationMatch = activeLocation === 'all' || itemLocation === activeLocation;
                    const itemTags = itemTag ? itemTag.split(',').map(t => t.trim()) : [];
                    const tagMatch = activeTags.has('all') || itemTags.some(t => activeTags.has(t));

                    if (locationMatch && tagMatch) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });
            });
        }

        // Attach logic to existing buttons
        document.querySelectorAll('.filter-btn').forEach(btn => attachFilterLogic(btn));

        // Dynamic Tag Fetching
        document.addEventListener('DOMContentLoaded', async () => {
            const allTags = new Set();
            const tagFiltersContent = document.querySelector('.tag-filters .dropdown-content');

            const fetchPromises = Array.from(gridItems).map(async (item) => {
                const url = item.getAttribute('href');
                if (!url) return;
                try {
                    const response = await fetch(url);
                    if (!response.ok) return;
                    const htmlText = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(htmlText, 'text/html');
                    
                    const tagElements = doc.querySelectorAll('.project-tags .tag');
                    const tags = Array.from(tagElements).map(t => t.textContent.replace(/^#/, '').trim()).filter(Boolean);

                    if (tags.length > 0) {
                        item.setAttribute('data-tag', tags.join(','));
                        tags.forEach(t => allTags.add(t));
                    }
                } catch (error) {
                    console.error(`Error fetching tags from ${url}:`, error);
                }
            });

            await Promise.all(fetchPromises);

            // Generate filter buttons
            allTags.forEach(tag => {
                const btn = document.createElement('button');
                btn.className = 'filter-btn';
                btn.setAttribute('data-type', 'tag');
                btn.setAttribute('data-filter', tag);
                btn.textContent = tag;
                
                attachFilterLogic(btn);
                tagFiltersContent.appendChild(btn);
            });
        });"""

html = re.sub(r'const filterBtns = document\.querySelectorAll.*?\}\);\s*\}\);', new_script, html, flags=re.DOTALL)

with open('works.html', 'w', encoding='utf-8') as f:
    f.write(html)

