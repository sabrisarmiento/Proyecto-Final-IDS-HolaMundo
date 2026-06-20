// const select = document.getElementById('select-courses');
// const container = document.getElementById('advertisements-container');
// const msg = document.getElementById('msg-select-course');

// if (select && container && msg) {
//   select.addEventListener('change', function () {
//     const courseId = this.value;

//     if (courseId === '') {
//       container.style.display = 'none';
//       msg.style.display = 'flex';
//       return;
//     }

//     container.style.display = 'flex';
//     msg.style.display = 'none';

//     const articles = container.querySelectorAll('article');

//     articles.forEach(article => {
//       if (article.dataset.course === courseId) {
//         article.style.display = 'block';
//       } else {
//         article.style.display = 'none';
//       }
//     });
//   });
// }

// const select = document.getElementById('select-courses');

// if (select) {
//   select.addEventListener('change', function () {
//     const courseId = this.value;
//     const params = new URLSearchParams(window.location.search);
//     const subjectId = params.get("subject");

//     if (courseId === '') {
//       window.location.href = `/avisos?subject=${subjectId}`;
//       return;
//     }

//     window.location.href = `/avisos?subject=${subjectId}&course=${courseId}`;
//   });
// }

const select = document.getElementById('select-courses');
const selectSource = document.getElementById('select-source');

if (select) {
  select.addEventListener('change', function () {
    const courseId = this.value;
    const params = new URLSearchParams(window.location.search);
    const subjectId = params.get("subject");

    if (courseId === '') {
      window.location.href = `/avisos?subject=${subjectId}`;
      return;
    }

    window.location.href = `/avisos?subject=${subjectId}&course=${courseId}&source=all`;
  });
}

if (selectSource) {
  selectSource.addEventListener('change', function () {
    const source = this.value;
    const params = new URLSearchParams(window.location.search);
    const subjectId = params.get("subject");
    const courseId = params.get("course");

    window.location.href = `/avisos?subject=${subjectId}&course=${courseId}&source=${source}`;
  });
}