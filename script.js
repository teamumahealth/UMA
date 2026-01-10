const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");
let width, height;
let stars = [];
let mouseX = 0;
let mouseY = 0;
let scrollOffset = 0;
window.addEventListener("scroll", () => {
    scrollOffset = window.scrollY;
});
function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();
window.addEventListener("mousemove", (e) => {
    mouseX = (e.clientX / width - 0.5) * 2;
    mouseY = (e.clientY / height - 0.5) * 2;
});
class Star{
    constructor(){
        this.reset();
    }
    reset(){
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.depth = Math.random() * 0.8 + 0.2;
        this.radius = Math.random() * 1.2 + this.depth * 1.2;
        this.speed = Math.random() * 0.3 + 0.1;
        this.alpha = 0.3 + this.depth * 0.6;
    }
    update(){
        this.y -= this.speed * (1 + this.depth * 0.5);
        this.x += mouseX * this.depth * 0.6;
        this.y += mouseY * this.depth * 0.6;
        this.y += scrollOffset * this.depth * 0.0008;

        if (
            this.y < -20 ||
            this.x < -20 ||
            this.x > width + 20 ||
            this.y > height + 20
        ) {
            this.y = height + 20;
            this.x = Math.random() * width;
        }
    }
    draw(){
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${this.alpha})`;
        ctx.fill();
    }
}
function initStars(count = 200) {
    stars = [];
    for (let i = 0; i < count; i++) {
        stars.push(new Star());
    }
}
function animateStars() {
    ctx.clearRect(0, 0, width, height);

    stars.forEach(star => {
        star.update();
        star.draw();
    });
    requestAnimationFrame(animateStars);
}
initStars(window.innerWidth < 768 ? 120 : 220);
animateStars();


