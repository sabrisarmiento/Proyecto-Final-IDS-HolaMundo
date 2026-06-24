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