// Main JavaScript for Dance Attendance Application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Kiosk mode functionality
    setupKioskMode();

    // Setup search functionality
    setupSearch();

    // Setup attendance marking animation
    setupAttendanceAnimation();
});

// Kiosk mode functionality
function setupKioskMode() {
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', function() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.error(`Error attempting to enable fullscreen mode: ${err.message}`);
                });
                fullscreenBtn.innerHTML = '<i class="fas fa-compress me-2"></i>Exit Fullscreen';
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                    fullscreenBtn.innerHTML = '<i class="fas fa-expand me-2"></i>Fullscreen Mode';
                }
            }
        });

        // Handle fullscreen change
        document.addEventListener('fullscreenchange', function() {
            if (!document.fullscreenElement) {
                fullscreenBtn.innerHTML = '<i class="fas fa-expand me-2"></i>Fullscreen Mode';
            }
        });

        // Auto-focus search field in kiosk mode
        const studentSearch = document.getElementById('studentSearch');
        if (studentSearch) {
            studentSearch.focus();
        }
    }
}

// Setup search functionality
function setupSearch() {
    const studentSearch = document.getElementById('studentSearch');
    if (studentSearch) {
        studentSearch.addEventListener('keyup', function() {
            const value = this.value.toLowerCase();
            const studentItems = document.querySelectorAll('.student-item');
            
            studentItems.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.indexOf(value) > -1) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Other search fields
    const otherSearchFields = ['classSearch', 'userSearch'];
    otherSearchFields.forEach(function(fieldId) {
        const searchField = document.getElementById(fieldId);
        if (searchField) {
            searchField.addEventListener('keyup', function() {
                const value = this.value.toLowerCase();
                const tableId = fieldId.replace('Search', 'Table');
                const rows = document.querySelectorAll(`#${tableId} tr`);
                
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    if (text.indexOf(value) > -1) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        }
    });
}

// Setup attendance marking animation
function setupAttendanceAnimation() {
    const attendanceForms = document.querySelectorAll('.attendance-form');
    
    attendanceForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            const studentCard = this.closest('.student-card');
            
            if (!studentCard.classList.contains('checked-in')) {
                e.preventDefault();
                
                // Disable button to prevent double submission
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Checking In...';
                
                // Add checked-in class for animation
                studentCard.classList.add('checked-in');
                
                // Add check icon if it doesn't exist
                if (!studentCard.querySelector('.check-icon')) {
                    const checkIcon = document.createElement('div');
                    checkIcon.className = 'check-icon';
                    checkIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
                    studentCard.appendChild(checkIcon);
                }
                
                // Change button text and style
                setTimeout(() => {
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-success');
                    button.innerHTML = '<i class="fas fa-check-circle me-2"></i>Already Checked In';
                    
                    // Change header style
                    const cardHeader = studentCard.querySelector('.card-header');
                    if (cardHeader) {
                        cardHeader.classList.remove('bg-primary');
                        cardHeader.classList.add('bg-success');
                    }
                    
                    // Submit the form after animation
                    setTimeout(() => {
                        form.submit();
                    }, 300);
                }, 700);
            }
        });
    });
}

// Handle date range selection in reports
function updateDateRange(range) {
    const today = new Date();
    let startDate = document.getElementById('start_date');
    let endDate = document.getElementById('end_date');
    
    if (!startDate || !endDate) return;
    
    endDate.valueAsDate = today;
    
    switch(range) {
        case 'today':
            startDate.valueAsDate = today;
            break;
        case 'week':
            const weekAgo = new Date(today);
            weekAgo.setDate(today.getDate() - 7);
            startDate.valueAsDate = weekAgo;
            break;
        case 'month':
            const monthAgo = new Date(today);
            monthAgo.setMonth(today.getMonth() - 1);
            startDate.valueAsDate = monthAgo;
            break;
        case 'year':
            const yearAgo = new Date(today);
            yearAgo.setFullYear(today.getFullYear() - 1);
            startDate.valueAsDate = yearAgo;
            break;
    }
}
