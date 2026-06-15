const select = document.getElementById('select-courses');
const container = document.getElementById('classes-container');
const msg = document.getElementById('msg-select-course');

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

function filterSchedule() {
  const text = document.getElementById("schedule-search").value.toLowerCase();
    document.querySelectorAll(".class").forEach(weekCard => {
        let visibleArticles = 0;
        weekCard.querySelectorAll("article").forEach(article => {
            const matches = article.dataset.search.includes(text);
            article.style.display = matches ? "flex" : "none";
            if (matches) visibleArticles++;
        });
        weekCard.style.display = visibleArticles > 0 ? "block" : "none";
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("select-courses");
  const search = document.getElementById("schedule-search");
  if (!select || !search) return;
  search.style.display = "none";
  select.addEventListener("change", () => {
    if (select.value !== "") {
      search.style.display = "block";
    } else {
      search.style.display = "none";
      search.value = "";
    }
  });
});