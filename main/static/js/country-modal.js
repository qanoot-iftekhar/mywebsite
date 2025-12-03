// Country Selection Modal
document.addEventListener('DOMContentLoaded', function () {
    const modalOverlay = document.getElementById('countryModalOverlay');
    const closeBtn = document.getElementById('countryModalClose');
    const confirmBtn = document.getElementById('countryConfirmBtn');
    const countrySelect = document.getElementById('countrySelect');

    // Check if user has already selected a country
    const hasSelectedCountry = localStorage.getItem('countrySelected');

    // Show modal only if user hasn't selected a country before
    if (!hasSelectedCountry) {
        setTimeout(() => {
            modalOverlay.classList.add('active');
        }, 500); // Small delay for better UX
    }

    // Close modal function
    function closeModal() {
        modalOverlay.classList.remove('active');
    }

    // Close button click
    closeBtn.addEventListener('click', closeModal);

    // Close on overlay click (outside modal)
    modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Confirm button click
    confirmBtn.addEventListener('click', function () {
        const selectedCountry = countrySelect.value;

        // Save to localStorage
        localStorage.setItem('countrySelected', 'true');
        localStorage.setItem('selectedCountry', selectedCountry);

        // Close modal
        closeModal();

        // Optional: You can add logic here to redirect or update the site based on country
        console.log('Selected country:', selectedCountry);
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });
});
