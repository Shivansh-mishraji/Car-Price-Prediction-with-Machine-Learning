document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const loadingState = document.getElementById('loading-state');
    const resultContainer = document.getElementById('result-container');
    const predictedPriceEl = document.getElementById('predicted-price');
    const resetBtn = document.getElementById('reset-btn');

    // API URL - change if hosted elsewhere
    const API_URL = '/predict';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Hide result, show loading
        form.classList.add('hidden');
        loadingState.classList.remove('hidden');

        // Gather data
        const formData = new FormData(form);
        const data = {
            Year: parseInt(formData.get('Year')),
            Present_Price: parseFloat(formData.get('Present_Price')),
            Driven_kms: parseInt(formData.get('Driven_kms')),
            Owner: parseInt(formData.get('Owner')),
            Fuel_Type: formData.get('Fuel_Type'),
            Transmission: formData.get('Transmission'),
            Selling_type: formData.get('Selling_type')
        };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const result = await response.json();
            
            // Format number to have commas for readability
            const formattedPrice = new Intl.NumberFormat('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(result.predicted_price_lakhs);

            predictedPriceEl.textContent = formattedPrice;

            // Animate number counting up (optional polish)
            animateValue(predictedPriceEl, 0, result.predicted_price_lakhs, 1000);

            // Hide loading, show result
            loadingState.classList.add('hidden');
            resultContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Prediction failed:', error);
            alert('Failed to get prediction. Ensure the backend server is running.');
            // Revert UI
            loadingState.classList.add('hidden');
            form.classList.remove('hidden');
        }
    });

    resetBtn.addEventListener('click', () => {
        resultContainer.classList.add('hidden');
        form.reset();
        form.classList.remove('hidden');
    });

    // Helper for number animation
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            // easeOutQuart
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            const currentVal = start + easeProgress * (end - start);
            
            obj.innerHTML = new Intl.NumberFormat('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(currentVal);
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
