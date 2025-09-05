document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const resultsSection = document.getElementById('results');
    const analysisResults = document.getElementById('analysis-results');
    
    // Load leaderboard on page load
    loadLeaderboard();
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const imageFile = document.getElementById('fridge-image').files[0];
        formData.append('fridge_image', imageFile);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            displayResults(data);
            resultsSection.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the image');
        });
    });
    
    function displayResults(data) {
        let html = `
            <h3>Item yang Terdeteksi</h3>
            <div class="item-list">
        `;
        
        data.detected_items.forEach(item => {
            const expiringClass = item.days_until_expiry <= 3 ? 'expiring' : '';
            html += `
                <div class="item-card ${expiringClass}">
                    <h4>${item.name}</h4>
                    <p>Jumlah: ${item.quantity}</p>
                    <p>Kadaluarsa dalam: ${item.days_until_expiry} hari</p>
                </div>
            `;
        });
        
        html += `</div>`;
        
        html += `
            <h3>Rekomendasi Resep</h3>
            <div class="recipe-list">
        `;
        
        data.recommended_recipes.forEach(recipe => {
            html += `
                <div class="recipe-card">
                    <h4>${recipe.name}</h4>
                    <p>Waktu persiapan: ${recipe.preparation_time} menit</p>
                    <p>Bahan: ${recipe.ingredients.join(', ')}</p>
                    <p>Instruksi: ${recipe.instructions}</p>
                </div>
            `;
        });
        
        html += `</div>`;
        
        html += `
            <div class="emission-summary">
                <h3>Dampak Lingkungan</h3>
                <p>Emisi yang dapat dihindari: <strong>${data.emission_results.avoided_emissions_kg} kg CO2</strong></p>
                <p>Item yang diselamatkan: <strong>${data.emission_results.items_saved} dari ${data.emission_results.total_items} item</strong></p>
                <p>Pemborosan yang dicegah: <strong>${data.emission_results.waste_prevented_percentage.toFixed(1)}%</strong></p>
                
                <button id="contribute-btn">Kontribusi ke Leaderboard</button>
            </div>
        `;
        
        analysisResults.innerHTML = html;
        
        document.getElementById('contribute-btn').addEventListener('click', function() {
            const username = prompt('Masukkan nama Anda untuk kontribusi ke leaderboard:');
            if (username) {
                contributeToLeaderboard(username, data.emission_results);
            }
        });
    }
    
    function contributeToLeaderboard(username, emissionResults) {
        fetch('/add_contribution', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                emission_results: emissionResults
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Terima kasih atas kontribusi Anda!');
                loadLeaderboard(); // Refresh leaderboard
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting your contribution');
        });
    }
    
    function loadLeaderboard() {
        fetch('/leaderboard')
        .then(response => response.json())
        .then(data => {
            displayLeaderboard(data);
        })
        .catch(error => {
            console.error('Error loading leaderboard:', error);
        });
    }
    
    function displayLeaderboard(data) {
        const leaderboardDiv = document.getElementById('leaderboard');
        let html = '<div class="leaderboard-list">';
        
        if (data.length === 0) {
            html += '<p>Belum ada kontributor. Jadilah yang pertama!</p>';
        } else {
            data.forEach((user, index) => {
                const topClass = index === 0 ? 'top-contributor' : '';
                html += `
                    <div class="leaderboard-item">
                        <span class="${topClass}">${index + 1}. ${user.username}</span>
                        <span class="${topClass}">${user.total_emissions_avoided.toFixed(1)} kg CO2</span>
                    </div>
                `;
            });
        }
        
        html += '</div>';
        leaderboardDiv.innerHTML = html;
    }
});