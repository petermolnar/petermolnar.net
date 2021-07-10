function isGalleryActive() {
    if ("#gallery" == window.location.hash) {
        return true;
    }
    else {
        return false;
    }
}

function setGalleryView(status) {
    var st = document.getElementById('css_gallery');
    if (isGalleryActive()) {
        st.setAttribute('media', 'all');
    }
    else {
        st.setAttribute('media', 'not all');
    }
}

function toggleGalleryView(e) {
    if(!isGalleryActive()) {
        window.location.hash = "#gallery";
    }
    else {
        window.location.hash = "#";
    }
    setGalleryView();
    return false;
}

function setupGalleryToggle() {
    var toggle = document.createElement('a');
    toggle.href = '#';
    toggle.onclick = toggleGalleryView;
    toggle.innerHTML = 'toggle gallery view'
    document.getElementById("gallery_toggle").appendChild(toggle);
    setGalleryView();
}

setupGalleryToggle();
