document.querySelectorAll('.category-option input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        this.form.submit();
    });
});