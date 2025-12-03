/**
 * Review Manager Class
 * Handles fetching, displaying, and submitting product reviews
 */
class ReviewManager {
    constructor(productId) {
        this.productId = productId;
        this.reviews = [];
        this.currentRating = 0;

        this.init();
    }

    init() {
        this.loadReviews();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Star rating input
        const stars = document.querySelectorAll('.star-rating-input i');
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                this.setRating(index + 1);
            });

            star.addEventListener('mouseenter', () => {
                this.highlightStars(index + 1);
            });
        });

        const ratingContainer = document.querySelector('.star-rating-input');
        if (ratingContainer) {
            ratingContainer.addEventListener('mouseleave', () => {
                this.highlightStars(this.currentRating);
            });
        }

        // Submit review form
        const submitBtn = document.getElementById('submit-review-btn');
        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.submitReview();
            });
        }
    }

    setRating(rating) {
        this.currentRating = rating;
        this.highlightStars(rating);
    }

    highlightStars(count) {
        const stars = document.querySelectorAll('.star-rating-input i');
        stars.forEach((star, index) => {
            if (index < count) {
                star.classList.remove('far');
                star.classList.add('fas', 'active');
            } else {
                star.classList.remove('fas', 'active');
                star.classList.add('far');
            }
        });
    }

    async loadReviews() {
        const reviewsList = document.getElementById('reviews-list');
        const reviewsSummary = document.getElementById('reviews-summary');

        if (!reviewsList) return;

        // Show loading
        reviewsList.innerHTML = `
            <div class="reviews-loading">
                <i class="fas fa-spinner"></i>
                <p>Loading reviews...</p>
            </div>
        `;

        try {
            const response = await fetch(`/api/reviews/?product_id=${this.productId}`);

            if (!response.ok) {
                throw new Error('Failed to load reviews');
            }

            const data = await response.json();
            this.reviews = data.results || data;

            if (this.reviews.length === 0) {
                reviewsList.innerHTML = `
                    <div class="reviews-empty">
                        <i class="far fa-comment-dots"></i>
                        <p>No reviews yet. Be the first to review this product!</p>
                    </div>
                `;
                if (reviewsSummary) {
                    reviewsSummary.style.display = 'none';
                }
            } else {
                this.renderReviews();
                this.renderSummary();
            }

        } catch (error) {
            console.error('Error loading reviews:', error);
            reviewsList.innerHTML = `
                <div class="reviews-empty">
                    <p>Failed to load reviews. Please try again later.</p>
                </div>
            `;
        }
    }

    renderReviews() {
        const reviewsList = document.getElementById('reviews-list');

        const html = this.reviews.map(review => this.createReviewCard(review)).join('');
        reviewsList.innerHTML = html;
    }

    createReviewCard(review) {
        const initial = review.user_name ? review.user_name.charAt(0).toUpperCase() : 'U';
        const userName = review.user_name || 'Anonymous';
        const date = new Date(review.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        return `
            <div class="review-card">
                <div class="review-header">
                    <div class="review-author">
                        <div class="review-avatar">${initial}</div>
                        <div class="review-author-info">
                            <h4>${userName}</h4>
                            <span class="review-date">${date}</span>
                        </div>
                    </div>
                    <div class="review-rating">
                        ${this.renderStars(review.rating)}
                    </div>
                </div>
                <p class="review-comment">${this.escapeHtml(review.comment)}</p>
            </div>
        `;
    }

    renderStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<i class="fas fa-star"></i>';
            } else {
                stars += '<i class="far fa-star"></i>';
            }
        }
        return stars;
    }

    renderSummary() {
        const summaryElement = document.getElementById('reviews-summary');
        if (!summaryElement) return;

        const avgRating = this.calculateAverageRating();
        const distribution = this.calculateRatingDistribution();

        summaryElement.innerHTML = `
            <div class="average-rating">
                <div class="rating-number">${avgRating.toFixed(1)}</div>
                <div class="rating-stars">${this.renderStars(Math.round(avgRating))}</div>
                <div class="rating-count">${this.reviews.length} review${this.reviews.length !== 1 ? 's' : ''}</div>
            </div>
            <div class="rating-distribution">
                ${this.renderDistribution(distribution)}
            </div>
        `;

        summaryElement.style.display = 'flex';
    }

    calculateAverageRating() {
        if (this.reviews.length === 0) return 0;
        const sum = this.reviews.reduce((acc, review) => acc + review.rating, 0);
        return sum / this.reviews.length;
    }

    calculateRatingDistribution() {
        const distribution = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
        this.reviews.forEach(review => {
            distribution[review.rating]++;
        });
        return distribution;
    }

    renderDistribution(distribution) {
        let html = '';
        for (let i = 5; i >= 1; i--) {
            const count = distribution[i];
            const percentage = this.reviews.length > 0 ? (count / this.reviews.length) * 100 : 0;
            html += `
                <div class="rating-bar">
                    <span class="rating-bar-label">${i} star${i !== 1 ? 's' : ''}</span>
                    <div class="rating-bar-fill">
                        <div class="rating-bar-fill-inner" style="width: ${percentage}%"></div>
                    </div>
                    <span class="rating-bar-count">${count}</span>
                </div>
            `;
        }
        return html;
    }

    async submitReview() {
        const commentInput = document.getElementById('review-comment');
        const submitBtn = document.getElementById('submit-review-btn');

        if (!commentInput || !submitBtn) return;

        const comment = commentInput.value.trim();

        // Validation
        if (this.currentRating === 0) {
            alert('Please select a rating');
            return;
        }

        if (comment.length < 10) {
            alert('Please write a review with at least 10 characters');
            return;
        }

        // Disable button
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        try {
            const response = await fetch('/api/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    product: this.productId,
                    rating: this.currentRating,
                    comment: comment
                })
            });

            if (response.ok) {
                // Success
                alert('Review submitted successfully!');

                // Reset form
                commentInput.value = '';
                this.currentRating = 0;
                this.highlightStars(0);

                // Reload reviews
                await this.loadReviews();

            } else if (response.status === 401 || response.status === 403) {
                alert('Please login to submit a review');
                window.location.href = `/login/?next=/product/${this.productId}/`;
            } else {
                const data = await response.json();
                alert('Failed to submit review: ' + (data.detail || 'Unknown error'));
            }

        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Failed to submit review. Please try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Review';
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize review manager when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    const productIdElement = document.getElementById('product-id');
    if (productIdElement) {
        const productId = productIdElement.value;
        window.reviewManager = new ReviewManager(productId);
    }
});
