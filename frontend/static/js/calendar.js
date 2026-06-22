document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("select-courses");
    const container = document.getElementById("classes-container");
    const msg = document.getElementById("msg-select-course");
    const search = document.getElementById("schedule-search");
    const noClassesMsg = document.getElementById("msg-no-classes");

    if (!select) return;

    function filter() {
        const courseId = select.value;
        const text = search ? search.value.toLowerCase().trim() : "";

        if (!courseId) {
            if (container) container.style.display = "none";
            if (msg) msg.style.display = "block";
            if (noClassesMsg) noClassesMsg.style.display = "none";
            if (search) { search.style.display = "none"; search.value = ""; }
            return;
        }

        if (container) container.style.display = "grid";
        if (msg) msg.style.display = "none";
        if (search) search.style.display = "block";

        let visibleWeeks = 0;

        document.querySelectorAll(".class").forEach(weekCard => {
            let visibleArticles = 0;

            weekCard.querySelectorAll("article").forEach(article => {
                const match = article.dataset.course === courseId && article.dataset.search.includes(text);
                article.style.display = match ? "flex" : "none";
                if (match) visibleArticles++;
            });

            const weekVisible = visibleArticles > 0;
            weekCard.style.display = weekVisible ? "block" : "none";
            if (weekVisible) visibleWeeks++;
        });

        if (noClassesMsg) noClassesMsg.style.display = visibleWeeks === 0 ? "block" : "none";
    }

    select.addEventListener("change", () => {
        if (search && select.value === "") search.value = "";
        filter();
    });

    if (search) search.addEventListener("input", filter);

    filter();
});