function emite_alerta() {
    alert("Python Rocks!");
};

logo = document.getElementsByTagName("img")[0];
logo.onclick = emite_alerta;