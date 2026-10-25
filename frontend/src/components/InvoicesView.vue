<template>
  <div class="flex-1 flex flex-col bg-white overflow-hidden h-full">
    <!-- Sticky Top Header -->
    <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shadow-2xs z-20 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-base font-bold text-gray-900">Sales Invoices</h2>
        <span class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-md">
          {{ filteredInvoices.length }} Total
        </span>
      </div>

      <div class="flex items-center gap-3">
        <div class="relative w-64 md:w-80">
          <span class="lucide-search absolute left-3 top-2.5 size-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search invoice or customer..."
            class="w-full pl-9 pr-7 py-1.5 text-xs bg-gray-50 hover:bg-white focus:bg-white border border-gray-200 rounded-[11px] focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2.5 top-2 text-gray-400 hover:text-gray-600 text-xs"
          >✕</button>
        </div>

        <div class="flex items-center gap-1.5 text-xs text-gray-600 bg-gray-50 border border-gray-200 rounded-[11px] px-2.5 py-1">
          <span class="text-gray-400 font-medium">From</span>
          <input v-model="fromDate" type="date" class="bg-transparent border-none text-xs text-gray-800 font-semibold focus:outline-none" />
          <span class="text-gray-300">|</span>
          <span class="text-gray-400 font-medium">To</span>
          <input v-model="toDate" type="date" class="bg-transparent border-none text-xs text-gray-800 font-semibold focus:outline-none" />
          <button v-if="fromDate || toDate" @click="fromDate = ''; toDate = ''" class="ml-1 text-gray-400 hover:text-gray-700 text-xs" title="Clear dates">✕</button>
        </div>
      </div>
    </header>

    <!-- Full Width Table -->
    <div class="flex-1 overflow-auto">
      <table class="w-full text-left text-sm border-collapse">
        <thead class="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200 text-xs uppercase sticky top-0 z-10 shadow-2xs">
          <tr>
            <th class="py-3.5 px-6 bg-gray-50">Invoice</th>
            <th class="py-3.5 px-6 bg-gray-50">Customer</th>
            <th class="py-3.5 px-6 bg-gray-50">Phone</th>
            <th class="py-3.5 px-6 bg-gray-50">Date</th>
            <th class="py-3.5 px-6 bg-gray-50">Modified</th>
            <th class="py-3.5 px-6 bg-gray-50">Status</th>
            <th class="py-3.5 px-6 bg-gray-50 text-right">Grand Total</th>
            <th class="py-3.5 px-6 bg-gray-50 text-center">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="inv in filteredInvoices"
            :key="inv.name"
            @click="openDetail(inv.name)"
            class="hover:bg-blue-50/40 transition cursor-pointer"
          >
            <td class="py-3 px-6 font-bold text-blue-600 font-mono">{{ inv.name }}</td>
            <td class="py-3 px-6 font-medium text-gray-900">{{ inv.customer_name || inv.customer }}</td>
            <td class="py-3 px-6 text-gray-500 text-xs font-mono">{{ inv.mobile_no || '—' }}</td>
            <td class="py-3 px-6 text-gray-500 text-xs">{{ formatDate(inv.posting_date) }}</td>
            <td class="py-3 px-6 text-gray-500 text-xs whitespace-nowrap">{{ formatDateTime(inv.modified) }}</td>
            <td class="py-3 px-6">
              <span
                class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                :class="inv.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
              >{{ inv.status }}</span>
            </td>
            <td class="py-3 px-6 text-right font-extrabold text-gray-900 text-base">
              ₹{{ Number(inv.grand_total).toFixed(2) }}
            </td>
            <td class="py-3 px-6 text-center" @click.stop>
              <button
                @click="openPrint(inv.name)"
                class="px-3 py-1.5 text-xs font-bold bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-[11px] transition inline-flex items-center gap-1.5 shadow-2xs border border-blue-200"
                title="Print Invoice"
              >
                <span class="lucide-printer size-3.5" />
                <span>Print</span>
              </button>
            </td>
          </tr>
          <tr v-if="filteredInvoices.length === 0">
            <td colspan="7" class="py-20 text-center text-gray-400">
              <div class="flex flex-col items-center justify-center">
                <span class="lucide-receipt size-9 text-gray-300 mb-2" />
                <p class="text-sm font-semibold text-gray-500">No invoices match your search or date filters</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Invoice Detail Modal -->
    <div
      v-if="showDetail"
      class="fixed inset-0 bg-black/50 backdrop-blur-xs flex items-center justify-center z-50 p-4"
      @click.self="showDetail = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl flex flex-col max-h-[90vh]">
        <!-- Modal Header -->
        <div class="px-5 py-3.5 border-b border-gray-200 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-2.5">
            <span class="lucide-receipt size-4 text-blue-600" />
            <h3 class="text-sm font-bold text-gray-900">{{ detailLoading ? 'Loading...' : detail?.name }}</h3>
            <span
              v-if="detail"
              class="px-2 py-0.5 rounded-full text-xs font-bold"
              :class="detail.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
            >{{ detail.status }}</span>
          </div>
          <button @click="showDetail = false" class="text-gray-400 hover:text-gray-700 text-lg leading-none">✕</button>
        </div>

        <div v-if="detailLoading" class="flex-1 flex items-center justify-center py-12">
          <span class="lucide-loader-2 size-6 text-blue-400 animate-spin" />
        </div>

        <div v-else-if="detail" class="flex-1 overflow-y-auto">
          <!-- Customer Info -->
          <div class="px-5 py-3 border-b border-gray-100 grid grid-cols-2 gap-3">
            <div>
              <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-0.5">Customer</p>
              <p class="text-sm font-bold text-gray-900">{{ detail.customer_name }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-0.5">Phone</p>
              <p class="text-sm font-bold text-gray-900">{{ detail.mobile_no || '—' }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-0.5">Date</p>
              <p class="text-sm font-bold text-gray-900">{{ formatDate(detail.posting_date) }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-0.5">Grand Total</p>
              <p class="text-base font-extrabold text-blue-600">₹{{ Number(detail.grand_total).toFixed(2) }}</p>
            </div>
          </div>

          <!-- Items Table -->
          <div class="px-5 pt-3 pb-1">
            <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-2">Items</p>
            <table class="w-full text-xs border-collapse">
              <thead>
                <tr class="border-b border-gray-200 text-gray-500">
                  <th class="pb-2 text-left font-semibold">Item</th>
                  <th class="pb-2 text-center font-semibold">Qty</th>
                  <th class="pb-2 text-right font-semibold">Rate</th>
                  <th class="pb-2 text-right font-semibold">Amount</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="row in detail.items" :key="row.item_code" class="hover:bg-gray-50">
                  <td class="py-2 pr-2">
                    <div class="font-semibold text-gray-900">{{ row.item_name || row.item_code }}</div>
                    <div class="text-[10px] text-gray-400 font-mono">{{ row.item_code }}</div>
                  </td>
                  <td class="py-2 text-center text-gray-700">{{ row.qty }} {{ row.uom }}</td>
                  <td class="py-2 text-right text-gray-700">₹{{ Number(row.rate).toFixed(2) }}</td>
                  <td class="py-2 text-right font-bold text-gray-900">₹{{ Number(row.amount).toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Payments -->
          <div v-if="detail.payments?.length" class="px-5 pt-2 pb-3">
            <p class="text-[11px] text-gray-400 font-semibold uppercase tracking-wider mb-1.5">Payment</p>
            <div class="flex gap-2 flex-wrap">
              <span
                v-for="p in detail.payments"
                :key="p.mode_of_payment"
                class="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded-[11px] text-xs font-bold"
              >
                {{ p.mode_of_payment }}: ₹{{ Number(p.amount).toFixed(2) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="px-5 py-3 border-t border-gray-200 flex justify-end gap-2 shrink-0">
          <button
            @click="showDetail = false"
            class="px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-[11px] font-medium"
          >Close</button>
          <button
            @click="showPrintPreview = true"
            class="px-4 py-1.5 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-[11px] shadow-xs flex items-center gap-1.5"
          >
            <span class="lucide-printer size-3.5" />
            Print Receipt
          </button>
        </div>
      </div>
    </div>

    <!-- Print Preview Modal (Frappe printview iframe) -->
    <div
      v-if="showPrintPreview && detail"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[60] p-4"
      @click.self="showPrintPreview = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl flex flex-col w-full max-w-4xl" style="height:92vh;">

        <!-- Header -->
        <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between shrink-0">
          <span class="text-sm font-bold text-gray-800 flex items-center gap-2">
            <span class="lucide-eye size-4 text-blue-500" />
            Print Preview — {{ detail.name }}
          </span>
          <button @click="showPrintPreview = false" class="text-gray-400 hover:text-gray-600 text-lg leading-none">✕</button>
        </div>

        <!-- Frappe printview iframe -->
        <iframe
          ref="printIframe"
          :src="`/printview?doctype=Sales%20Invoice&name=${encodeURIComponent(detail.name)}&format=Standard&no_letterhead=0&_lang=en`"
          class="flex-1 w-full border-0 bg-white"
        />

        <!-- Actions -->
        <div class="px-4 py-3 border-t border-gray-200 flex justify-end gap-2 shrink-0">
          <button @click="showPrintPreview = false"
            class="px-4 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-[11px] font-medium border border-gray-200">Close</button>
          <button @click="doPrint"
            class="px-5 py-1.5 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-[11px] flex items-center gap-1.5">
            <span class="lucide-printer size-3.5" />
            Print
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  invoices: { type: Array, default: () => [] },
});

const emit = defineEmits(['print']);

const searchQuery = ref('');
const fromDate = ref('');
const toDate = ref('');
const showDetail = ref(false);
const detailLoading = ref(false);
const detail = ref(null);

function formatDate(date) {
  if (!date) return '—';
  const [y, m, d] = String(date).split('-');
  return `${d}-${m}-${y}`;
}

function formatDateTime(dt) {
  if (!dt) return '—';
  const d = new Date(String(dt).replace(' ', 'T'));
  if (isNaN(d)) return String(dt);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yy = d.getFullYear();
  let h = d.getHours();
  const min = String(d.getMinutes()).padStart(2, '0');
  const ampm = h >= 12 ? 'PM' : 'AM';
  h = h % 12 || 12;
  return `${dd}-${mm}-${yy} ${h}:${min} ${ampm}`;
}

const filteredInvoices = computed(() => {
  return props.invoices.filter((inv) => {
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchName = (inv.name || '').toLowerCase().includes(q);
      const matchCustomer = (inv.customer_name || inv.customer || '').toLowerCase().includes(q);
      const matchMobile = (inv.mobile_no || '').includes(q);
      if (!matchName && !matchCustomer && !matchMobile) return false;
    }
    if (fromDate.value && inv.posting_date && inv.posting_date < fromDate.value) return false;
    if (toDate.value && inv.posting_date && inv.posting_date > toDate.value) return false;
    return true;
  });
});

async function openDetail(name) {
  showDetail.value = true;
  detailLoading.value = true;
  detail.value = null;
  try {
    const res = await fetch('/api/method/tailorms.api.get_invoice_detail', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({ invoice_name: name }),
    });
    const json = await res.json();
    detail.value = json.message || null;
  } catch {
    detail.value = null;
  } finally {
    detailLoading.value = false;
  }
}

const showPrintPreview = ref(false);
const printIframe = ref(null);

function printInvoice(name) {
  emit('print', name);
}

async function openPrint(name) {
  if (!detail.value || detail.value.name !== name) {
    detailLoading.value = true;
    detail.value = null;
    try {
      const res = await fetch('/api/method/tailorms.api.get_invoice_detail', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
        body: JSON.stringify({ invoice_name: name }),
      });
      const json = await res.json();
      detail.value = json.message || null;
    } catch {
      detail.value = null;
    } finally {
      detailLoading.value = false;
    }
  }
  if (detail.value) showPrintPreview.value = true;
}

function doPrint() {
  const iframe = printIframe.value;
  if (iframe && iframe.contentWindow) {
    iframe.contentWindow.focus();
    iframe.contentWindow.print();
  }
}
</script>
