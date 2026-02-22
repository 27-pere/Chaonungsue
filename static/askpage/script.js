const days = document.getElementsByName("work_days");

days.forEach(day => {
  day.addEventListener("click", () => {
    console.log(day.value);
  });
});
