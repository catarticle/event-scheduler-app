document.addEventListener('DOMContentLoaded', function() {
    // Управление категориями
    const allCategories = document.getElementById('all-categories');
    const categoryCheckboxes = document.querySelectorAll('.category-checkbox');
    
    allCategories.addEventListener('change', function() {
        if(this.checked) {
            categoryCheckboxes.forEach(cb => cb.checked = false);
        }
    });
    
    categoryCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if(this.checked) {
                allCategories.checked = false;
            }
        });
    });
    
    // Управление городами
    const allCities = document.querySelector('input[name="city"][value="all"]');
    const cityCheckboxes = document.querySelectorAll('input[name="city"]:not([value="all"])');
    
    allCities.addEventListener('change', function() {
        if(this.checked) {
            cityCheckboxes.forEach(cb => cb.checked = false);
        }
    });
    
    cityCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if(this.checked) {
                allCities.checked = false;
            }
        });
    });
});