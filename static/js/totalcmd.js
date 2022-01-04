STV_LIST = 'list';
STV_OPEN = 'open';
STV_RENAME = 'rename';
STV_MKDIR = 'mkdir';
STV_MKFILE = 'mkfile';
API_ACTION = '/totalcmd/action'
DOM_LPANEL = document.getElementById('l_side');
DOM_RPANEL = document.getElementById('r_side');
MAP_ATRIBUTES = {
    'id': '',
    'name': 'Name',
    'owner': "Owner",
    'perm': "Permisions",
    'size': "Size",
    'atime': "Last Accesed",
    'mtime': "Lat Modified",
    'ctime': "Created Time",
    'str_atime': "Last Accesed",
    'str_mtime': "Lat Modified",
    'str_ctime': "Created Time"
}

MAP_ICONFILES = {
    'dir': '/static/png/folder.png',
    'file': '/static/png/file.png'
}

/**
 * Get specific cookie value.
 * 
 * @since 0.2.0
 *
 * @param {String} c_name Key
 * 
 * @return {String} Cookie value if exist else empty string
 */
 function getCookie(c_name) {
    if (document.cookie.length > 0) {
        let c_start = document.cookie.indexOf(c_name + "=");
        if (c_start !== -1) {
            c_start = c_start + c_name.length + 1;
            let c_end = document.cookie.indexOf(";", c_start);
            if (c_end === -1) c_end = document.cookie.length;
            return decodeURI(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
  }

async function startUpServices() {
    getList();

    displayListPanel(DOM_LPANEL);
    displayListPanel(DOM_RPANEL);
}

document.addEventListener('DOMContentLoaded', startUpServices, false);

function displayPathParts(dnode, parts) {
    dnode.innerHTML = "";
    parts.forEach( p => {
        let el = document.createElement('span');
        el.className = "path-node";
        el.innerHTML = p.name;
        el.addEventListener('click', () => {
            displayListPanel(dnode.parentElement, p.id, false);
        });
        dnode.appendChild(el);
    })
}

function getAtributes(sample) {
    if (sample) {
        let atributes = ['id' , 'name']
                        .concat(Object.keys(sample))
                        .map(x => MAP_ATRIBUTES[x] || '')
                        .filter(onlyUnique);
        // save atributes;
        return atributes;
    }
}

function displayFilesHeader(header, sample) {
    let tr = header.querySelector('tr');
    tr.innerHTML = "";
    getAtributes(sample).forEach(a => {
        let el = document.createElement('td');
        el.innerHTML = a;
        tr.appendChild(el);
    })
}

function createFileRow(data, panel) {
    let container = document.createElement('tr');
    container.className = 'file-item';
    container.dataset.type = data.type

    // show img col
    let img_container = document.createElement('td');
    container.appendChild(img_container);
    img_container.dataset.role = 'type';
    let icon = document.createElement('img');
    img_container.appendChild(icon);
    icon.alt = "";
    icon.style.width = "60%";
    icon.src = MAP_ICONFILES[data.type] || '';

    let name_container = document.createElement('td');
    container.appendChild(name_container);
    name_container.dataset.role = 'name';
    name_container.innerHTML = data.name;
    if ( data.type === 'dir') {
        name_container.addEventListener('click', () => {
            displayListPanel(panel, data.id, false);
        }, false);
    }
    if ( data.type === 'file') {
        name_container.addEventListener('click', () => {
            openFileNode(data.id);
        });
    }

    let used_list = ['id' , 'name', 'type'];
    Object.keys(data).filter( i => !used_list.includes(i)).forEach( i => {
        let atr_container = document.createElement('td');
        atr_container.innerHTML = data[i];
        container.appendChild(atr_container);
    });
    return container;
}

function openRenameInput(dnode, pathid) {
    let old_container = dnode.querySelector('td[data-role=name]');
    let container = document.createElement('td');
    let input = document.createElement('input');
    container.appendChild(input);
    input.value = old_container.innerHTML
    input.style.width = '80%';

    old_container.after(container);
    old_container.remove();

    let btn = document.createElement('button');
    container.appendChild(btn);
    btn.textContent = "ok";
    btn.addEventListener('click', () => {
        renameFileNode(pathid, input.value).then( r => {
            // to something if error or succes
            let p = dnode;
            while (p && ![...p.classList].includes('side')) {
                p = p.parentNode;
            }
            if(r.ok) {
                container.after(old_container);
                old_container.innerHTML = input.value;
                container.remove();
                if ( r.content.type === 'dir') {
                    old_container.addEventListener('click', () => {
                        displayListPanel(p, r.content.id, false);
                    }, false);
                }
                if ( r.content.type === 'file') {
                    old_container.addEventListener('click', () => {
                        openFileNode(r.content.id);
                    });
                }
            }
            else {
                container.after(old_container);
                container.remove();
                // do error showing
                
                old_container.innerHTML = input.value;
                if ( dnode.dataset.type === 'dir') {
                    old_container.addEventListener('click', () => {
                        displayListPanel(p, pathid, false);
                    }, false);
                }
                if ( dnode.dataset.type === 'file') {
                    old_container.addEventListener('click', () => {
                        openFileNode(pathid);
                    });
                }
            }
        });
    });
}

function displayListPanel(panel, id, reload_atribues = true,reload_path = true,) {
    getList(id).then(c => {
        if(c.ok) {
            let table = panel.querySelector('table');
            let tbody = table.querySelector('tbody');
            let first_element = tbody.firstChild;
            tbody.innerHTML = "";
            tbody.appendChild(first_element);
            c = c.content;
            if (reload_path) {
                displayPathParts(panel.querySelector(".path"), c.parts);
                tbody.innerHTML = "";
                let p_dict = {};
                Object.keys(c.parent).forEach( i => {
                    p_dict[i] = '';
                });
                p_dict.type = 'dir';
                p_dict.id = c.parent.id;
                p_dict.name = "..";

                let tr = createFileRow(p_dict, panel);
                tbody.appendChild(tr);
                panel.dataset.cwp = c.parent.id;
            }
            if ( reload_atribues) {
                displayFilesHeader(table.querySelector('thead'), c.files[0]);
            }
            
            c.files.forEach(i => {
                let tr = createFileRow(i, panel);
                tbody.appendChild(tr);
                
                tr.addEventListener('contextmenu', e => {
                    e.preventDefault();
                    
                    new Contextual({
                        isSticky: false,
                        items: [
                            {label: 'Open', onClick: () => {
                                if ( i.type === 'dir') {
                                    displayListPanel(panel, i.id, false);
                                }
                                if ( data.type === 'file') {
                                    openFileNode(i.id);
                                }
                            }, shortcut: 'Ctrl+O'},
                            {label: 'Rename', onClick: () => {
                                openRenameInput(tr, i.id);
                            }, shortcut: 'Ctrl+B'},
                            {type: 'seperator'},
                            {label: 'Copy', onClick: () => {}, shortcut: 'Ctrl+A'},
                            {label: 'Move', onClick: () => {}, shortcut: 'Ctrl+A'},
                            {type: 'hovermenu', label: 'new', items: [
                                {label: 'Folder', onClick: () => {
                                    makeNewFolder(tr);
                                }},
                                {label: 'File', onClick: () => {
                                    makeNewFile(tr);
                                }},
                            ]},
                        ]
                    });
                })
            });

        } else {
            // error handleing
        }
    })
}

async function makeNewFile(provider) {
    let p = provider;
    while (p && ![...p.classList].includes('side')) {
        p = p.parentNode;
    }
    let name = prompt("Please enter file name", "New File");
    let form = new FormData();
    form.append('action', STV_MKFILE);
    form.append('node', p.dataset.cwp);
    form.append('value', name);
    return await fetch(API_ACTION, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: form
    }).then(r => r.json()).then(r => {
        if(r.ok) {
            displayListPanel(p, p.dataset.cwp, false);
        }
    });
}

async function makeNewFolder(provider) {
    let p = provider;
    while (p && ![...p.classList].includes('side')) {
        p = p.parentNode;
    }
    let name = prompt("Please enter folder name", "New Folder");
    let form = new FormData();
    form.append('action', STV_MKDIR);
    form.append('node', p.dataset.cwp);
    form.append('value', name);
    return await fetch(API_ACTION, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: form
    }).then(r => r.json()).then(r => {
        if(r.ok) {
            displayListPanel(p, p.dataset.cwp, false);
        }
    });
}

async function renameFileNode(pathid, name) {
    let form = new FormData();
    form.append('action', STV_RENAME);
    form.append('node', pathid);
    form.append('value', name);
    return await fetch(API_ACTION, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: form
    }).then(r => r.json());
}

function openFileNode(pathid) {
    let form = new FormData();
    form.append('action', STV_OPEN);
    form.append('node', pathid);
    return fetch(API_ACTION, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: form
    }).then(r => r.json()).then( r => {
        // to something if error or succes
    });
}

async function getList(pathid = null) {
    let form = new FormData();
    form.append('action', STV_LIST);
    form.append('atrs', ["owner", "size", "str_atime", "perm"]);
    if( pathid !== null) {
        form.append('node', pathid);
    }
    return await fetch(API_ACTION, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: form
    }).then(r => r.json());
}

