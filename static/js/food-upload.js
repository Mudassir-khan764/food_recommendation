/**
 * Food Object Detection - Multi-item detection with detailed nutrition analysis
 * Displays: Detected Food, Quantity, Calories per item, Total Calories
 */

// Food emoji mapping for visual representation
const foodEmojiMap = {
    'apple': '🍎', 'banana': '🍌', 'orange': '🍊', 'gulab_jamun': '🍮',
    'pizza': '🍕', 'burger': '🍔', 'chicken': '🍗', 'fish': '🐟',
    'egg': '🥚', 'salad': '🥗', 'rice': '🍚', 'bread': '🍞',
    'cheese': '🧀', 'ice_cream': '🍦', 'donut': '🍩', 'cake': '🎂',
    'curry': '🍛', 'naan': '🫓', 'soup': '🍲', 'coffee': '☕',
    'unknown': '🍽️'
};

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('foodImage');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeImage = document.getElementById('removeImage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadForm = document.getElementById('foodUploadForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const detectionResults = document.getElementById('detectionResults');
    const errorAlert = document.getElementById('errorAlert');
    const detectionCanvas = document.getElementById('detectionCanvas');

    // Drag and drop functionality
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Remove image
    removeImage.addEventListener('click', clearImage);

    // Form submission
    uploadForm.addEventListener('submit', handleFormSubmit);

    // Analyze Another button
    document.getElementById('analyzeAnotherBtn').addEventListener('click', () => {
        clearImage();
        detectionResults.style.display = 'none';
        document.getElementById('uploadSection').style.display = 'block';
    });

    // Add to Meal Plan button
    document.getElementById('addToMealPlanBtn').addEventListener('click', () => {
        alert('This would add detected items to your meal plan. Feature coming soon!');
    });

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#764ba2';
        uploadArea.style.background = 'linear-gradient(135deg, #e9ecef 0%, #b8c6db 100%)';
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
    }

    function handleDrop(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    }

    function handleFile(file) {
        // Validate file type
        if (!file.type.match(/^image\/(jpeg|jpg|png)$/)) {
            showError('Please select a valid image file (JPG, PNG)');
            return;
        }

        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
            showError('File size must be less than 5MB');
            return;
        }

        // Display preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            
            uploadArea.style.display = 'none';
            imagePreview.style.display = 'block';
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function clearImage() {
        fileInput.value = '';
        imagePreview.style.display = 'none';
        uploadArea.style.display = 'block';
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
        analyzeBtn.disabled = true;
        previewImg.src = '';
        errorAlert.style.display = 'none';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        
        if (!fileInput.files[0]) {
            showError('Please select an image first');
            return;
        }

        // Show loading
        imagePreview.style.display = 'none';
        uploadArea.style.display = 'none';
        loadingSpinner.style.display = 'block';
        errorAlert.style.display = 'none';

        // Prepare form data
        const formData = new FormData();
        formData.append('food_image', fileInput.files[0]);

        // Submit to backend
        fetch('/upload-food-image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = 'none';
            
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'Detection failed');
                imagePreview.style.display = 'block';
                uploadArea.style.display = 'block';
            }
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            showError('Network error. Please try again.');
            console.error('Error:', error);
            imagePreview.style.display = 'block';
            uploadArea.style.display = 'block';
        });
    }

    function displayResults(data) {
        // Display image with bounding boxes
        const img = new Image();
        img.onload = function() {
            detectionCanvas.width = img.width;
            detectionCanvas.height = img.height;
            const ctx = detectionCanvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            drawBoundingBoxes(ctx, data.detections, data.image_dimensions);
        };
        img.src = 'data:image/png;base64,' + data.image_with_boxes;

        // Calculate summary statistics
        const totalDetections = (data.nutrition_summary || []).reduce((sum, item) => sum + item.quantity, 0);
        const totalCalories = (data.nutrition_summary || []).reduce((sum, item) => sum + item.total_calories, 0);
        const uniqueFoods = (data.nutrition_summary || []).length;

        // Update summary
        document.getElementById('totalDetections').textContent = totalDetections;
        document.getElementById('totalCaloriesSummary').innerHTML = totalCalories.toFixed(0) + '<span style="font-size: 0.6em; margin-left: 5px;">kcal</span>';
        document.getElementById('uniqueFoodsCount').textContent = uniqueFoods;
        document.getElementById('detectionBadge').textContent = `${totalDetections} item${totalDetections !== 1 ? 's' : ''} detected`;

        // Display detailed nutrition breakdown
        displayNutritionSummary(data.nutrition_summary || []);

        // Show results section
        detectionResults.style.display = 'block';
        document.getElementById('uploadSection').style.display = 'none';
    }

    function drawBoundingBoxes(ctx, detections, imageDimensions) {
        const colors = [
            '#FF6B6B',  // Red
            '#4ECDC4',  // Teal
            '#45B7D1',  // Blue
            '#FFA07A',  // Light Salmon
            '#98D8C8',  // Mint
            '#F7DC6F',  // Yellow
            '#BB8FCE',  // Purple
            '#85C1E2',  // Sky Blue
        ];

        detections.forEach((detection, idx) => {
            const bbox = detection.bbox;
            const color = colors[idx % colors.length];
            const lineWidth = 3;

            // Draw rectangle
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.strokeRect(bbox.x1, bbox.y1, bbox.x2 - bbox.x1, bbox.y2 - bbox.y1);

            // Draw label
            const label = formatFoodName(detection.food_name) + ` (${(detection.confidence * 100).toFixed(0)}%)`;
            const fontSize = 16;
            ctx.font = `bold ${fontSize}px Arial`;
            const textWidth = ctx.measureText(label).width;

            // Draw label background
            ctx.fillStyle = color;
            ctx.fillRect(bbox.x1, bbox.y1 - fontSize - 10, textWidth + 15, fontSize + 10);

            // Draw label text
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText(label, bbox.x1 + 8, bbox.y1 - 2);
        });
    }

    function displayNutritionSummary(nutritionSummary) {
        const container = document.getElementById('nutritionDetailsList');
        container.innerHTML = '';

        if (!nutritionSummary || nutritionSummary.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999;">No foods detected</p>';
            return;
        }

        // Group by food name for aggregated display
        const groupedFood = {};
        nutritionSummary.forEach(item => {
            const foodName = item.food_name || 'unknown';
            if (!groupedFood[foodName]) {
                groupedFood[foodName] = {
                    quantity: 0,
                    calories_per_item: item.calories_per_item || 0,
                    total_calories: 0,
                    average_confidence: 0,
                    count: 0,
                    unit: item.unit || 'piece'
                };
            }
            groupedFood[foodName].quantity += item.quantity || 1;
            groupedFood[foodName].total_calories += item.total_calories || 0;
            groupedFood[foodName].average_confidence += item.average_confidence || 0;
            groupedFood[foodName].count += 1;
        });

        // Calculate average confidence
        Object.keys(groupedFood).forEach(food => {
            groupedFood[food].average_confidence = groupedFood[food].average_confidence / groupedFood[food].count;
        });

        // Display each food item
        Object.entries(groupedFood).forEach(([foodName, data], idx) => {
            const emoji = getEmoji(foodName);
            const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'];
            const color = colors[idx % colors.length];
            const confidencePercent = Math.round(data.average_confidence * 100);

            const foodCard = document.createElement('div');
            foodCard.className = 'food-item';
            foodCard.innerHTML = `
                <div class="food-info">
                    <div class="food-emoji">${emoji}</div>
                    <div class="food-details">
                        <h4>${formatFoodName(foodName)}</h4>
                        <p style="color: #999; font-size: 0.85rem;">Per item: ${Math.round(data.calories_per_item)} kcal | Confidence: ${confidencePercent}%</p>
                    </div>
                </div>
                <div class="food-stats">
                    <div class="stat-box">
                        <div class="stat-label">Quantity</div>
                        <div class="stat-value">${data.quantity}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Per Item</div>
                        <div class="stat-value">${Math.round(data.calories_per_item)}<span class="detail-unit">kcal</span></div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Total</div>
                        <div class="stat-value">${Math.round(data.total_calories)}<span class="detail-unit">kcal</span></div>
                    </div>
                </div>
            `;

            // Add confidence progress bar
            const progressHTML = `
                <div class="progress-container">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 0.85rem; color: #999; font-weight: 600;">Detection Confidence</span>
                        <span style="font-size: 0.9rem; font-weight: 700; color: ${color};">${confidencePercent}%</span>
                    </div>
                    <div class="progress-bar-custom">
                        <div class="progress-fill" style="width: ${confidencePercent}%; background: ${color};"></div>
                    </div>
                </div>
            `;

            const progressDiv = document.createElement('div');
            progressDiv.innerHTML = progressHTML;
            foodCard.appendChild(progressDiv);

            container.appendChild(foodCard);
        });
    }

    function formatFoodName(name) {
        return name
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    function getEmoji(foodName) {
        const name = foodName.toLowerCase();
        return foodEmojiMap[name] || '🍽️';
    }

    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
        uploadArea.style.display = 'block';
        imagePreview.style.display = 'none';
        loadingSpinner.style.display = 'none';
        detectionResults.style.display = 'none';
    }
});
