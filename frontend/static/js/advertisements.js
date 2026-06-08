const select = document.getElementById('select-courses');
const container = document.getElementById('advertisements-container');
const msg = document.getElementById('msg-select-course');

if (select && container && msg) {
  select.addEventListener('change', function () {
    const courseId = this.value;

    if (courseId === '') {
      container.style.display = 'none';
      msg.style.display = 'flex';
      return;
    }

    container.style.display = 'flex';
    msg.style.display = 'none';

    const articles = container.querySelectorAll('article');

    articles.forEach(article => {
      if (article.dataset.course === courseId) {
        article.style.display = 'block';
      } else {
        article.style.display = 'none';
      }
    });
  });
}