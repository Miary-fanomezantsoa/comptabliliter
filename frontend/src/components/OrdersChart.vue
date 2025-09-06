<template>
  <div>
    <canvas ref="ordersChart"></canvas>
  </div>
</template>

<script>
import { onMounted, ref, watch } from "vue";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  props: ["orders"],
  setup(props) {
    const ordersChart = ref(null);
    let chartInstance = null;

    // Fonction pour extraire les mois dynamiquement
    const getMonthlyData = (orders) => {
      const dataMap = {}; // { '2025-01': 5, '2025-02': 3, ... }

      orders.forEach((order) => {
        const date = new Date(order.date); // Assure-toi que 'date' existe
        const key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}`;
        if (!dataMap[key]) dataMap[key] = 0;
        dataMap[key]++;
      });

      const labels = Object.keys(dataMap).sort();
      const data = labels.map((label) => dataMap[label]);

      return { labels, data };
    };

    const renderChart = () => {
      if (!ordersChart.value) return;

      const { labels, data } = getMonthlyData(props.orders);

      if (chartInstance) chartInstance.destroy(); // Détruire ancien chart
      chartInstance = new Chart(ordersChart.value, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Commandes",
              data,
              backgroundColor: "rgba(255, 165, 0, 0.7)",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
          },
        },
      });
    };

    watch(() => props.orders, renderChart, { immediate: true });

    onMounted(renderChart);

    return { ordersChart };
  },
};
</script>
