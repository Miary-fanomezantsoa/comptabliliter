<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script>
import { onMounted, watch, ref } from "vue";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "StatsChart",
  props: {
    labels: Array,
    data: Array,
    type: { type: String, default: "line" },
    label: String,
    color: String,
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    const renderChart = () => {
      if (chartInstance) {
        chartInstance.destroy(); // détruit l’ancien chart
      }
      if (!chartCanvas.value) return; // vérifie que le canvas existe

      chartInstance = new Chart(chartCanvas.value, {
        type: props.type,
        data: {
          labels: props.labels,
          datasets: [
            {
              label: props.label,
              data: props.data,
              backgroundColor: props.color,
              borderColor: props.color,
              fill: props.type === "line",
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: true } },
        },
      });
    };

    onMounted(() => renderChart());

    // Re-render si les données changent
    watch(
      () => [props.labels, props.data],
      () => renderChart(),
      { deep: true }
    );

    return { chartCanvas };
  },
};
</script>
