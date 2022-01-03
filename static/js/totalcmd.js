STV_LIST = 'list';
API_ACTION = '/totalcmd/action'

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

async function startUpServices() {
    getList();
}

document.addEventListener('DOMContentLoaded', startUpServices, false);

async function getList(pathid = null) {
    let form = new FormData();
    form.append('action', STV_LIST);
    form.append('atrs', ["owner", "str_atime"]);
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

