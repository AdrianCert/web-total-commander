STV_LIST = 'list';
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
    name_container.innerHTML = data.name;
    if ( data.type === 'dir') {
        name_container.addEventListener('click', () => {
            displayListPanel(panel, data.id, false);
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
                Object.keys(c.files[0]).forEach( i => {
                    p_dict[i] = '';
                });
                p_dict.type = 'dir';
                p_dict.id = c.parent;
                p_dict.name = "..";

                let tr = createFileRow(p_dict, panel);
                tbody.appendChild(tr);
            }
            if ( reload_atribues) {
                displayFilesHeader(table.querySelector('thead'), c.files[0]);
            }
            
            c.files.forEach(i => {
                tbody.appendChild(createFileRow(i, panel));
            });

        } else {
            // error handleing
        }
    })
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

