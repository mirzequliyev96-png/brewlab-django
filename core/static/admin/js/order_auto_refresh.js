(function() {
    if (window.location.pathname.includes('/admin/core/order/')) {
        setInterval(function() {
            if (!document.querySelector('.submit-row')) {
                location.reload();
            }
        }, 5000);
    }
})();