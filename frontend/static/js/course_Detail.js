function switchTab(tabName, btnEl) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.subnav-btn').forEach(b => b.classList.remove('active'));

    document.getElementById('tab-' + tabName).classList.remove('hidden');
    btnEl.classList.add('active');
}