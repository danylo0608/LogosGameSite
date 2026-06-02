// Global database data
let DB_DATA = {};
let currentFilters = {};

/**
 * Loads the SQLite database and populates DB_DATA
 */
async function loadDatabase() {
    const sqlPromise = initSqlJs({
        locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/${file}`
    });
    
    // Convert Base64 string to Uint8Array
    const binaryString = atob(SQLITE_DB_BASE64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }

    const SQL = await sqlPromise;
    const db = new SQL.Database(bytes);

    const tables = [
        'game_game', 'game_category', 'game_playercountrange', 'game_agegroup',
        'game_gameduration', 'game_preplevel', 'game_location', 'game_activitylevel',
        'game_interactiontype', 'game_gamegoal', 'game_contenttype', 'game_thematic',
        'game_sitesettings'
    ];

    // Helper to convert DB results to array of objects
    const queryToObjects = (sql) => {
        const res = db.exec(sql);
        if (res.length === 0) return [];
        const columns = res[0].columns;
        return res[0].values.map(row => {
            const obj = {};
            columns.forEach((col, i) => obj[col] = row[i]);
            return obj;
        });
    };

    // Load simple tables
    tables.forEach(table => {
        DB_DATA[table] = queryToObjects(`SELECT * FROM ${table}`);
    });

    // Load ManyToMany relationships
    const m2m_tables = [
        { field: 'categories', table: 'game_game_categories', id_col: 'category_id' },
        { field: 'players_ranges', table: 'game_game_players_ranges', id_col: 'playercountrange_id' },
        { field: 'age_groups', table: 'game_game_age_groups', id_col: 'agegroup_id' },
        { field: 'durations', table: 'game_game_durations', id_col: 'gameduration_id' },
        { field: 'prep_levels', table: 'game_game_prep_levels', id_col: 'preplevel_id' },
        { field: 'locations', table: 'game_game_locations', id_col: 'location_id' },
        { field: 'activity_levels', table: 'game_game_activity_levels', id_col: 'activitylevel_id' },
        { field: 'interaction_types', table: 'game_game_interaction_types', id_col: 'interactiontype_id' },
        { field: 'goals', table: 'game_game_goals', id_col: 'gamegoal_id' },
        { field: 'content_types', table: 'game_game_content_types', id_col: 'contenttype_id' },
        { field: 'thematics', table: 'game_game_thematics', id_col: 'thematic_id' }
    ];

    // Attach M2M data to games
    DB_DATA['game_game'].forEach(game => {
        m2m_tables.forEach(m2m => {
            const results = db.exec(`SELECT ${m2m.id_col} FROM ${m2m.table} WHERE game_id = ${game.id}`);
            game[m2m.field] = results.length > 0 ? results[0].values.map(v => v[0]) : [];
        });
    });

    db.close();
    console.log("Database loaded successfully from SQLite file");
}

// Initial Render for index.html
document.addEventListener('DOMContentLoaded', async () => {
    if (document.getElementById('filterContainer')) {
        try {
            await loadDatabase();
            renderFilters();
            applyCurrentFilters();
            
            // Mobile toggle logic
            const toggleBtn = document.getElementById('mobileFilterToggle');
            const sidebar = document.getElementById('filterSidebar');
            if (toggleBtn && sidebar) {
                toggleBtn.addEventListener('click', () => {
                    sidebar.classList.toggle('show');
                    sidebar.classList.toggle('d-none');
                });
            }
        } catch (error) {
            console.error("Initialization error:", error);
            const list = document.getElementById('gameList');
            if (list) list.innerHTML = `<div class="col-12 alert alert-danger">Помилка завантаження бази даних: ${error.message}</div>`;
        }
    }
});

function renderFilters() {
    const container = document.getElementById('filterContainer');
    if (!container) return;

    const filterSpecs = [
        { key: 'goals', label: 'Ситуація', table: 'game_gamegoal' },
        { key: 'players_ranges', label: 'Гравців', table: 'game_playercountrange' },
        { key: 'age_groups', label: 'Вік', table: 'game_agegroup' },
        { key: 'durations', label: 'Тривалість', table: 'game_gameduration' },
        { key: 'prep_levels', label: 'Підготовка', table: 'game_preplevel' },
        { key: 'activity_levels', label: 'Активність', table: 'game_activitylevel' },
        { key: 'locations', label: 'Місце', table: 'game_location' },
        { key: 'interaction_types', label: 'Взаємодія', table: 'game_interactiontype' },
        { key: 'content_types', label: 'Контент', table: 'game_contenttype' },
        { key: 'thematics', label: 'Тематика', table: 'game_thematic' }
    ];

    container.innerHTML = filterSpecs.map(spec => {
        const options = DB_DATA[spec.table] || [];
        return `
            <div class="mb-4">
                <label class="form-label small text-muted text-uppercase fw-bold ls-1 mb-2 d-block">${spec.label}</label>
                <div class="custom-dropdown" id="dropdown-${spec.key}">
                    <div class="dropdown-trigger" onclick="toggleDropdown('${spec.key}')">
                        <span class="selected-text" id="selected-${spec.key}">Всі</span>
                        <i class="bi bi-chevron-down"></i>
                    </div>
                    <div class="dropdown-menu-custom">
                        <div class="dropdown-option active" onclick="selectOption('${spec.key}', null, 'Всі')">Всі</div>
                        ${options.map(opt => `
                            <div class="dropdown-option" onclick="selectOption('${spec.key}', ${opt.id}, '${opt.name}')">${opt.name}</div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function toggleDropdown(key) {
    const el = document.getElementById(`dropdown-${key}`);
    const isOpen = el.classList.contains('open');
    document.querySelectorAll('.custom-dropdown').forEach(d => d.classList.remove('open'));
    if (!isOpen) el.classList.add('open');
}

function selectOption(key, id, name) {
    const dropdown = document.getElementById(`dropdown-${key}`);
    dropdown.querySelectorAll('.dropdown-option').forEach(opt => opt.classList.remove('active'));
    
    // Find clicked option
    const options = dropdown.querySelectorAll('.dropdown-option');
    options.forEach(opt => {
        if (opt.innerText === name) opt.classList.add('active');
    });

    document.getElementById(`selected-${key}`).innerText = name;
    if (id === null) {
        delete currentFilters[key];
    } else {
        currentFilters[key] = id;
    }
    dropdown.classList.remove('open');
}

document.getElementById('applyFilters')?.addEventListener('click', () => {
    applyCurrentFilters();
});

document.getElementById('resetFilters')?.addEventListener('click', (e) => {
    e.preventDefault();
    currentFilters = {};
    renderFilters();
    applyCurrentFilters();
});

function applyCurrentFilters() {
    let games = DB_DATA.game_game;

    Object.keys(currentFilters).forEach(key => {
        const val = currentFilters[key];
        games = games.filter(game => {
            const gameVal = game[key];
            if (Array.isArray(gameVal)) {
                return gameVal.includes(val);
            }
            return gameVal === val;
        });
    });

    renderGameList(games);
}

function renderGameList(games) {
    const container = document.getElementById('gameList');
    if (!container) return;

    document.getElementById('gameCount').innerText = games.length;

    if (games.length === 0) {
        container.innerHTML = `
            <div class="col-12 py-5 text-center">
                <div class="p-5 rounded-4" style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1);">
                    <i class="bi bi-search mb-3 d-block text-muted" style="font-size: 3rem;"></i>
                    <h3 class="text-white">Ігор не знайдено</h3>
                    <p class="text-muted">За вказаними фільтрами поки немає результатів.</p>
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = games.map(game => {
        // Отримуємо назви всіх цілей (goals)
        const goals = (game.goals && game.goals.length > 0) 
            ? game.goals.map(id => DB_DATA.game_gamegoal.find(g => g.id === id)?.name).filter(n => n)
            : ['Гра'];
        
        // Отримуємо назви всіх тематик (thematics)
        const thematics = (game.thematics && game.thematics.length > 0)
            ? game.thematics.map(id => DB_DATA.game_thematic.find(t => t.id === id)?.name).filter(n => n)
            : [];

        const duration = (game.durations && game.durations.length > 0)
            ? game.durations.map(id => DB_DATA.game_gameduration.find(d => d.id === id)?.name).filter(n => n).join(', ')
            : '-';
            
        const players = (game.players_ranges && game.players_ranges.length > 0)
            ? game.players_ranges.map(id => DB_DATA.game_playercountrange.find(p => p.id === id)?.name).filter(n => n).join(', ')
            : '-';

        return `
            <div class="col-lg-4 col-md-6">
                <div class="card game-card p-4 d-flex flex-column position-relative">
                    <a href="game.html?id=${game.id}" class="stretched-link"></a>
                    <div class="mb-2 d-flex flex-wrap gap-2">
                        ${goals.map(goal => `<span class="badge badge-primary rounded-pill px-3" style="font-size: 0.75rem;">${goal}</span>`).join('')}
                        ${thematics.map(t => `<span class="badge bg-info bg-opacity-10 text-info rounded-pill px-3" style="font-size: 0.75rem;">${t}</span>`).join('')}
                    </div>
                    <h5 class="card-title text-white fw-bold mb-3" style="font-size: 1.1rem;">${game.title}</h5>
                    <p class="card-text text-white-50 small flex-grow-1 mb-4" style="line-height: 1.6;">
                        ${game.description.substring(0, 80)}...
                    </p>
                    <div class="mt-auto pt-3 border-top border-secondary border-opacity-10">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="text-muted small d-flex align-items-center gap-1"><i class="bi bi-clock text-primary"></i> ${duration}</span>
                            <span class="text-muted small d-flex align-items-center gap-1"><i class="bi bi-people text-primary"></i> ${players}</span>
                        </div>
                        
                        ${game.show_external && game.external_link ? `
                        <a href="${game.external_link}" target="_blank" class="btn btn-success w-100 py-2 rounded-pill fw-bold position-relative" style="z-index: 2;">
                            <i class="bi bi-globe me-2"></i> ${game.external_text || 'Грати онлайн'}
                        </a>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function renderGameDetail(id) {
    const container = document.getElementById('gameDetail');
    if (!container) return;

    const game = DB_DATA.game_game.find(g => g.id === id);
    if (!game) {
        container.innerHTML = "<h1>Гра не знайдена</h1>";
        return;
    }

    // Helper to get multiple names
    const getNames = (ids, table) => {
        if (!ids || ids.length === 0) return null;
        return ids.map(id => DB_DATA[table].find(t => t.id === id)?.name).filter(n => n).join(', ');
    };

    const categories = getNames(game.categories, 'game_category');
    const goals = getNames(game.goals, 'game_gamegoal');
    const durations = getNames(game.durations, 'game_gameduration');
    const players = getNames(game.players_ranges, 'game_playercountrange');
    const age = getNames(game.age_groups, 'game_agegroup');
    const prep = getNames(game.prep_levels, 'game_preplevel');
    const location = getNames(game.locations, 'game_location');
    const activity = getNames(game.activity_levels, 'game_activitylevel');
    const interaction = getNames(game.interaction_types, 'game_interactiontype');
    const content = getNames(game.content_types, 'game_contenttype');
    const thematic = getNames(game.thematics, 'game_thematic');

    const paramsHtml = `
        <div class="card card-glass p-4 mb-4">
            <h4 class="h5 mb-4 border-bottom border-secondary pb-3">Параметри гри</h4>
            <div class="d-flex flex-column gap-4">
                ${renderParam('bi-people', 'Гравці', players)}
                ${renderParam('bi-person-badge', 'Вік', age)}
                ${renderParam('bi-clock', 'Тривалість', durations)}
                ${renderParam('bi-tools', 'Підготовка', prep)}
                ${renderParam('bi-geo-alt', 'Місце', location)}
                ${renderParam('bi-lightning', 'Активність', activity)}
                ${renderParam('bi-diagram-3', 'Взаємодія', interaction)}
                ${renderParam('bi-box', 'Тип контенту', content)}
                ${renderParam('bi-tag', 'Тематика', thematic)}
                ${renderParam('bi-star', 'Розвиває', game.skill_developed)}
            </div>

            <div class="mt-4 pt-4 border-top border-secondary border-opacity-25 d-flex flex-column gap-2">
                ${game.show_tg && game.tg_link ? `<a href="${game.tg_link}" target="_blank" class="btn btn-primary w-100 py-3 fw-bold"><i class="bi bi-telegram me-2"></i> ${game.tg_text || 'Перейти в чат гри'}</a>` : ''}
                ${game.show_external && game.external_link ? `<a href="${game.external_link}" target="_blank" class="btn btn-outline-primary w-100 py-3 fw-bold"><i class="bi bi-globe me-2"></i> ${game.external_text || 'Грати онлайн'}</a>` : ''}
            </div>
        </div>
    `;

    container.innerHTML = `
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="index.html" class="text-primary text-decoration-none">Головна</a></li>
                <li class="breadcrumb-item active text-white-50">${game.title}</li>
            </ol>
        </nav>

        <div class="row">
            <div class="col-lg-8">
                <!-- Блок 1: Про гру -->
                <div class="card card-glass p-4 p-md-5 mb-4">
                    <div class="mb-4">
                        ${categories ? `<span class="badge bg-secondary badge-pill me-2">${categories}</span>` : ''}
                        <span class="badge bg-primary badge-pill">${goals || 'Гра'}</span>
                    </div>
                    <h1 class="display-4 fw-bold mb-4">${game.title}</h1>
                    <h4 class="h5 text-primary mb-3">Про гру</h4>
                    <p class="lead text-white-50">${game.description}</p>
                </div>

                <!-- Блок 2 (Mobile only): Параметри між Описом та Правилами -->
                <div class="d-lg-none">
                    ${paramsHtml}
                </div>

                <!-- Блок 3: Правила та хід гри -->
                <div class="card card-glass p-4 p-md-5 mb-4">
                    <h4 class="h5 text-primary mb-4 border-bottom border-secondary pb-3">Правила та хід гри</h4>
                    <div class="text-white-50 lh-lg" style="white-space: pre-wrap; font-size: 1.1rem;">${game.rules}</div>
                </div>
            </div>

            <!-- Блок 2 (Desktop): Параметри справа -->
            <div class="col-lg-4 d-none d-lg-block">
                <div class="sticky-lg-top" style="top: 20px;">
                    ${paramsHtml}
                </div>
            </div>
        </div>
    `;
}

function renderParam(icon, label, value) {
    if (!value) return '';
    return `
        <div class="d-flex align-items-center gap-3">
            <div class="param-icon"><i class="bi ${icon}"></i></div>
            <div>
                <span class="d-block small text-muted">${label}</span>
                <span class="fw-bold">${value}</span>
            </div>
        </div>
    `;
}
