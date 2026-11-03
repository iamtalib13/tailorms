<template>
  <div class="flex-1 flex flex-col bg-white overflow-hidden h-full">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shadow-2xs z-20 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-base font-bold text-gray-900">Customers</h2>
        <span class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-md">
          {{ filteredCustomers.length }} Total
        </span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Search bar -->
        <div class="relative w-64 md:w-80">
          <span class="lucide-search absolute left-3 top-2.5 size-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search customer name or mobile..."
            class="w-full pl-9 pr-7 py-1.5 text-xs bg-gray-50 hover:bg-white focus:bg-white border border-gray-200 rounded-[11px] focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2.5 top-2 text-gray-400 hover:text-gray-600 text-xs"
          >✕</button>
        </div>

        <button
          @click="fetchCustomers"
          :disabled="loading"
          class="px-3 py-1.5 text-xs font-semibold bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded-lg flex items-center gap-1.5 transition"
        >
          <span :class="loading ? 'animate-spin' : ''" class="lucide-refresh-cw size-3.5" />
          Refresh
        </button>
      </div>
    </header>

    <!-- Table -->
    <div class="flex-1 overflow-auto">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-gray-50/90 backdrop-blur-xs sticky top-0 z-10 border-b border-gray-200 text-gray-500 font-semibold uppercase tracking-wider text-[11px]">
          <tr>
            <th class="py-3 px-6">Customer</th>
            <th class="py-3 px-6">Mobile</th>
            <th class="py-3 px-6 text-center">Invoices</th>
            <th class="py-3 px-6 text-right">Total Spent</th>
            <th class="py-3 px-6 text-right">Outstanding</th>
            <th class="py-3 px-6 text-center">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 font-medium text-gray-700">
          <tr
            v-for="c in filteredCustomers"
            :key="c.name"
            @click="openCustomerDetail(c.name)"
            class="hover:bg-blue-50/40 transition cursor-pointer group"
          >
            <!-- Customer Name & Group -->
            <td class="py-3.5 px-6">
              <div class="flex items-center gap-2.5">
                <div class="size-8 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-xs shrink-0">
                  {{ (c.customer_name || c.name || '?').charAt(0).toUpperCase() }}
                </div>
                <div>
                  <div class="font-bold text-gray-900 group-hover:text-blue-600 transition">
                    {{ c.customer_name || c.name }}
                  </div>
                  <div class="text-[10.5px] text-gray-400">
                    {{ c.customer_group || 'All Customer Groups' }}
                  </div>
                </div>
              </div>
            </td>

            <!-- Mobile -->
            <td class="py-3.5 px-6">
              <span v-if="c.mobile_no" class="font-mono text-gray-800 font-semibold">{{ c.mobile_no }}</span>
              <span v-else class="text-gray-400 italic">No mobile</span>
            </td>

            <!-- Total Invoices count -->
            <td class="py-3.5 px-6 text-center">
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-gray-100 text-gray-700">
                {{ c.total_invoices || 0 }}
              </span>
            </td>

            <!-- Total Spent -->
            <td class="py-3.5 px-6 text-right font-bold text-gray-900">
              ₹{{ formatCurrency(c.total_spent) }}
            </td>

            <!-- Outstanding -->
            <td class="py-3.5 px-6 text-right">
              <span
                v-if="Number(c.total_outstanding || 0) > 0"
                class="font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded"
              >
                ₹{{ formatCurrency(c.total_outstanding) }}
              </span>
              <span v-else class="text-emerald-600 font-medium">₹0.00</span>
            </td>

            <!-- Action -->
            <td class="py-3.5 px-6 text-center" @click.stop>
              <button
                @click="openCustomerDetail(c.name)"
                class="px-2.5 py-1 text-xs font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg transition"
              >
                View History
              </button>
            </td>
          </tr>

          <!-- Empty State -->
          <tr v-if="!loading && filteredCustomers.length === 0">
            <td colspan="6" class="py-16 text-center text-gray-400">
              <div class="flex flex-col items-center justify-center gap-2">
                <span class="lucide-users size-8 text-gray-300" />
                <p class="font-semibold text-gray-500 text-sm">No customers found</p>
                <p class="text-xs text-gray-400">Try adjusting your search criteria</p>
              </div>
            </td>
          </tr>

          <!-- Loading State -->
          <tr v-if="loading && filteredCustomers.length === 0">
            <td colspan="6" class="py-16 text-center text-gray-400">
              <div class="flex items-center justify-center gap-2">
                <span class="lucide-loader-2 size-5 animate-spin text-blue-600" />
                <span>Loading customers...</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Customer Detail Modal (Popup with Blurred Backdrop) -->
    <div
      v-if="activeCustomer"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs transition-opacity"
      @click.self="closeCustomerModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-gray-100 w-full max-w-5xl max-h-[92vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <!-- Modal Top Header -->
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gradient-to-r from-gray-50 to-white shrink-0">
          <div class="flex items-center gap-3">
            <div class="size-11 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-base shadow-sm">
              {{ (activeCustomer.customer_name || activeCustomer.name || '?').charAt(0).toUpperCase() }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base font-bold text-gray-900">
                  {{ activeCustomer.customer_name || activeCustomer.name }}
                </h3>
                <span v-if="activeCustomer.mobile_no" class="px-2 py-0.5 rounded-full text-[11px] font-mono bg-blue-50 text-blue-700 font-semibold border border-blue-100">
                  {{ activeCustomer.mobile_no }}
                </span>
              </div>
              <p class="text-xs text-gray-500 mt-0.5">
                Customer since {{ formatDate(activeCustomer.creation) }}
              </p>
            </div>
          </div>

          <button
            @click="closeCustomerModal"
            class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
            title="Close"
          >
            ✕
          </button>
        </div>

        <!-- Quick Summary Cards -->
        <div class="grid grid-cols-3 gap-4 px-6 py-3.5 bg-gray-50/70 border-b border-gray-200 shrink-0">
          <div class="bg-white p-3 rounded-xl border border-gray-200/80 shadow-2xs">
            <div class="text-[10.5px] font-semibold text-gray-400 uppercase">Total Invoices</div>
            <div class="text-xl font-black text-gray-800 mt-0.5">
              {{ activeCustomer.invoices ? activeCustomer.invoices.length : 0 }}
            </div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-gray-200/80 shadow-2xs">
            <div class="text-[10.5px] font-semibold text-gray-400 uppercase">Total Purchased</div>
            <div class="text-xl font-black text-emerald-600 mt-0.5">
              ₹{{ formatCurrency(customerTotalPurchased) }}
            </div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-gray-200/80 shadow-2xs">
            <div class="text-[10.5px] font-semibold text-gray-400 uppercase">Outstanding</div>
            <div class="text-xl font-black mt-0.5" :class="customerTotalOutstanding > 0 ? 'text-red-600' : 'text-gray-800'">
              ₹{{ formatCurrency(customerTotalOutstanding) }}
            </div>
          </div>
        </div>

        <!-- Main Body: Two Pane (Left: Invoices List, Right: Quick Invoice Detail) -->
        <div class="flex-1 overflow-hidden flex divide-x divide-gray-200">
          <!-- Left: Invoices List -->
          <div class="flex-1 overflow-auto p-5">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="text-xs font-bold text-gray-700 uppercase tracking-wider">
                Invoices ({{ (activeCustomer.invoices || []).length }})
              </h4>
              <span class="text-[11px] text-gray-400">Click row for quick details</span>
            </div>

            <div v-if="loadingDetail" class="py-12 text-center text-gray-400 flex items-center justify-center gap-2">
              <span class="lucide-loader-2 size-5 animate-spin text-blue-600" />
              <span>Loading customer invoices...</span>
            </div>

            <table v-else-if="(activeCustomer.invoices || []).length > 0" class="w-full text-left text-xs border-collapse">
              <thead class="bg-gray-100 text-gray-600 font-semibold uppercase text-[10.5px] sticky top-0 z-10">
                <tr>
                  <th class="py-2.5 px-3 rounded-l-lg">Invoice ID</th>
                  <th class="py-2.5 px-3">Date</th>
                  <th class="py-2.5 px-3">Status</th>
                  <th class="py-2.5 px-3 text-right">Amount</th>
                  <th class="py-2.5 px-3 text-center rounded-r-lg">Print</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="inv in activeCustomer.invoices"
                  :key="inv.name"
                  @click="loadInvoiceQuickDetail(inv.name)"
                  :class="selectedInvoiceName === inv.name ? 'bg-blue-50/80 ring-1 ring-blue-500/30' : 'hover:bg-gray-50/80'"
                  class="transition font-medium cursor-pointer"
                >
                  <td class="py-2.5 px-3 font-bold text-gray-900 font-mono flex items-center gap-1.5">
                    <span
                      class="size-1.5 rounded-full"
                      :class="selectedInvoiceName === inv.name ? 'bg-blue-600 ring-2 ring-blue-200' : 'bg-transparent'"
                    />
                    {{ inv.name }}
                  </td>
                  <td class="py-2.5 px-3 text-gray-600">{{ formatDate(inv.posting_date) }}</td>
                  <td class="py-2.5 px-3">
                    <span
                      class="px-2 py-0.5 rounded-full text-[10px] font-bold"
                      :class="inv.status === 'Paid' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'"
                    >
                      {{ inv.status || (inv.docstatus === 1 ? 'Submitted' : 'Draft') }}
                    </span>
                  </td>
                  <td class="py-2.5 px-3 text-right font-bold text-gray-900">
                    ₹{{ formatCurrency(inv.grand_total) }}
                  </td>
                  <td class="py-2.5 px-3 text-center" @click.stop>
                    <button
                      @click="$emit('print', inv.name)"
                      class="px-2 py-0.5 text-[11px] font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 rounded transition"
                    >
                      Print
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <div v-else class="py-12 text-center text-gray-400">
              No invoices found for this customer.
            </div>
          </div>

          <!-- Right: Quick Invoice Detail Pane -->
          <div class="w-80 lg:w-96 flex flex-col bg-gray-50/50 shrink-0 overflow-hidden">
            <div v-if="selectedInvoiceLoading" class="flex-1 flex items-center justify-center text-gray-400 gap-2">
              <span class="lucide-loader-2 size-5 animate-spin text-blue-600" />
              <span class="text-xs">Loading invoice items...</span>
            </div>

            <div v-else-if="selectedInvoiceDetail" class="flex-1 flex flex-col overflow-hidden">
              <!-- Invoice Detail Header -->
              <div class="p-4 border-b border-gray-200 bg-white shrink-0 flex items-center justify-between">
                <div>
                  <div class="text-[10.5px] font-semibold text-gray-400 uppercase">Selected Invoice</div>
                  <div class="font-bold font-mono text-sm text-gray-900">{{ selectedInvoiceDetail.name }}</div>
                </div>
                <button
                  @click="$emit('print', selectedInvoiceDetail.name)"
                  class="px-2.5 py-1 text-xs font-semibold bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg transition"
                >
                  Print PDF
                </button>
              </div>

              <!-- Quick Info List -->
              <div class="p-4 border-b border-gray-200 bg-white grid grid-cols-2 gap-2 text-xs shrink-0">
                <div>
                  <span class="text-gray-400 text-[10.5px] block">Date</span>
                  <span class="font-semibold text-gray-800">{{ formatDate(selectedInvoiceDetail.posting_date) }}</span>
                </div>
                <div>
                  <span class="text-gray-400 text-[10.5px] block">Status</span>
                  <span class="font-bold text-emerald-600">{{ selectedInvoiceDetail.status }}</span>
                </div>
                <div class="col-span-2 pt-1 border-t border-gray-100 flex items-center justify-between">
                  <span class="text-gray-500 font-medium">Grand Total</span>
                  <span class="font-black text-base text-blue-600">₹{{ formatCurrency(selectedInvoiceDetail.grand_total) }}</span>
                </div>
              </div>

              <!-- Item Lines -->
              <div class="flex-1 overflow-auto p-4">
                <div class="text-[11px] font-bold text-gray-600 uppercase mb-2">
                  Items ({{ selectedInvoiceDetail.items?.length || 0 }})
                </div>
                <div class="space-y-2">
                  <div
                    v-for="(itm, idx) in selectedInvoiceDetail.items"
                    :key="idx"
                    class="p-2.5 bg-white border border-gray-200 rounded-lg shadow-2xs text-xs"
                  >
                    <div class="font-bold text-gray-800">{{ itm.item_name || itm.item_code }}</div>
                    <div class="text-[10.5px] text-gray-400 font-mono">{{ itm.item_code }}</div>
                    <div class="flex items-center justify-between mt-1 text-gray-600">
                      <span>{{ itm.qty }} {{ itm.uom }} × ₹{{ formatCurrency(itm.rate) }}</span>
                      <span class="font-bold text-gray-900">₹{{ formatCurrency(itm.amount) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Payments -->
                <div v-if="selectedInvoiceDetail.payments?.length" class="mt-4 pt-3 border-t border-gray-200">
                  <div class="text-[11px] font-bold text-gray-600 uppercase mb-2">Payment Modes</div>
                  <div class="space-y-1">
                    <div
                      v-for="(pm, pIdx) in selectedInvoiceDetail.payments"
                      :key="pIdx"
                      class="flex items-center justify-between text-xs text-gray-700 bg-white p-2 rounded border border-gray-100"
                    >
                      <span class="font-medium">{{ pm.mode_of_payment }}</span>
                      <span class="font-bold text-gray-900">₹{{ formatCurrency(pm.amount) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty Selection State -->
            <div v-else class="flex-1 flex flex-col items-center justify-center p-6 text-center text-gray-400">
              <span class="lucide-receipt size-8 text-gray-300 mb-1" />
              <p class="text-xs font-semibold text-gray-500">No invoice selected</p>
              <p class="text-[11px] text-gray-400">Click on any invoice row from left to view details</p>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-3 border-t border-gray-200 bg-gray-50 flex items-center justify-between shrink-0">
          <span class="text-xs text-gray-400">Press <kbd class="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-[10px] font-mono shadow-2xs">Esc</kbd> to close</span>
          <button
            @click="closeCustomerModal"
            class="px-4 py-1.5 text-xs font-bold text-gray-700 bg-white border border-gray-200 hover:bg-gray-100 rounded-lg shadow-2xs transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const emit = defineEmits(['print']);

const customers = ref([]);
const loading = ref(false);
const searchQuery = ref('');

const activeCustomer = ref(null);
const loadingDetail = ref(false);

const selectedInvoiceName = ref('');
const selectedInvoiceDetail = ref(null);
const selectedInvoiceLoading = ref(false);

const filteredCustomers = computed(() => {
  if (!searchQuery.value.trim()) return customers.value;
  const q = searchQuery.value.toLowerCase().trim();
  return customers.value.filter((c) =>
    (c.customer_name || c.name || '').toLowerCase().includes(q) ||
    (c.mobile_no || '').includes(q)
  );
});

const customerTotalPurchased = computed(() => {
  if (!activeCustomer.value || !activeCustomer.value.invoices) return 0;
  return activeCustomer.value.invoices.reduce((sum, inv) => sum + (Number(inv.grand_total) || 0), 0);
});

const customerTotalOutstanding = computed(() => {
  if (!activeCustomer.value || !activeCustomer.value.invoices) return 0;
  return activeCustomer.value.invoices.reduce((sum, inv) => sum + (Number(inv.outstanding_amount) || 0), 0);
});

function formatCurrency(val) {
  return Number(val || 0).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatDate(d) {
  if (!d) return '—';
  try {
    return new Date(d).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return d;
  }
}

async function fetchCustomers() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_customer_list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      customers.value = json.message;
    }
  } catch (err) {
    console.error('Failed to load customers', err);
  } finally {
    loading.value = false;
  }
}

async function openCustomerDetail(customerName) {
  loadingDetail.value = true;
  selectedInvoiceName.value = '';
  selectedInvoiceDetail.value = null;
  activeCustomer.value = { name: customerName, customer_name: customerName, invoices: [] };
  try {
    const res = await fetch('/api/method/tailorms.api.get_customer_details', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({ customer: customerName }),
    });
    const json = await res.json();
    if (json.message) {
      activeCustomer.value = json.message;
    }
  } catch (err) {
    console.error('Failed to load customer details', err);
  } finally {
    loadingDetail.value = false;
  }
}

async function loadInvoiceQuickDetail(invoiceName) {
  selectedInvoiceName.value = invoiceName;
  selectedInvoiceLoading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_invoice_detail', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({ invoice_name: invoiceName }),
    });
    const json = await res.json();
    if (json.message) {
      selectedInvoiceDetail.value = json.message;
    }
  } catch (err) {
    console.error('Failed to load invoice detail', err);
  } finally {
    selectedInvoiceLoading.value = false;
  }
}

function closeCustomerModal() {
  activeCustomer.value = null;
  selectedInvoiceName.value = '';
  selectedInvoiceDetail.value = null;
}

function handleEscKey(e) {
  if (e.key === 'Escape' && activeCustomer.value) {
    closeCustomerModal();
  }
}

onMounted(() => {
  fetchCustomers();
  document.addEventListener('keydown', handleEscKey);
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscKey);
});
</script>
