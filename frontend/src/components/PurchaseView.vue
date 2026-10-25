<template>
  <div class="flex-1 flex flex-col bg-white overflow-hidden h-full">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shadow-2xs z-20 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-base font-bold text-gray-900">Purchase Entries</h2>
        <span class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-md">
          {{ entries.length }} Total
        </span>
      </div>
      <div class="flex gap-2">
        <button
          @click="openForm"
          class="px-3 py-1.5 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-xs flex items-center gap-1.5"
        >
          <span class="lucide-plus size-3.5" />
          New Entry
        </button>
        <button
          @click="$emit('refresh')"
          class="px-3 py-1.5 text-xs font-semibold bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50"
        >Refresh</button>
      </div>
    </header>

    <!-- Entries Table -->
    <div class="flex-1 overflow-auto">
      <table class="w-full text-left text-sm border-collapse">
        <thead class="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200 text-xs uppercase sticky top-0 z-10 shadow-2xs">
          <tr>
            <th class="py-3.5 px-6 bg-gray-50">Entry ID</th>
            <th class="py-3.5 px-6 bg-gray-50">Supplier</th>
            <th class="py-3.5 px-6 bg-gray-50">Type</th>
            <th class="py-3.5 px-6 bg-gray-50">Date</th>
            <th class="py-3.5 px-6 bg-gray-50">Status</th>
            <th class="py-3.5 px-6 bg-gray-50 text-right">Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="stk in entries"
            :key="stk.name"
            @click="openDetail(stk.name)"
            class="hover:bg-blue-50/40 transition cursor-pointer"
          >
            <td class="py-3 px-6 font-bold text-blue-600 font-mono">{{ stk.name }}</td>
            <td class="py-3 px-6 font-medium text-gray-900">{{ stk.supplier_name || stk.supplier || '—' }}</td>
            <td class="py-3 px-6 text-gray-500 text-xs">{{ stk.stock_entry_type || stk.purpose }}</td>
            <td class="py-3 px-6 text-gray-500 text-xs">{{ formatDate(stk.posting_date) }}</td>
            <td class="py-3 px-6">
              <span
                class="px-2.5 py-0.5 rounded-full text-xs font-bold"
                :class="stk.docstatus === 1 ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'"
              >{{ stk.docstatus === 1 ? 'Submitted' : 'Draft' }}</span>
            </td>
            <td class="py-3 px-6 text-right font-extrabold text-gray-900">
              ₹{{ Number(stk.total_amount || 0).toFixed(2) }}
            </td>
          </tr>
          <tr v-if="entries.length === 0">
            <td colspan="6" class="py-20 text-center text-gray-400">
              <div class="flex flex-col items-center justify-center">
                <span class="lucide-package size-9 text-gray-300 mb-2" />
                <p class="text-sm font-semibold text-gray-500">No purchase entries found</p>
                <button @click="openForm" class="mt-3 px-3 py-1.5 text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200">
                  + Create First Entry
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- New Purchase Entry Modal — Frappe v16 style -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
      @click.self="showForm = false"
    >
      <div class="bg-white flex flex-col w-full max-w-3xl shadow-2xl rounded-lg border border-gray-300" style="height: 90vh;">

        <!-- Frappe-style title bar -->
        <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between shrink-0 bg-white rounded-t-lg">
          <div class="flex items-center gap-2.5">
            <div class="flex items-center gap-2">
              <span class="text-xs text-gray-400">Stock Entry</span>
              <span class="text-gray-300 text-xs">›</span>
              <span class="text-sm font-semibold text-gray-800">{{ formEntryName || 'New Purchase Entry' }}</span>
            </div>
            <span v-if="formDocstatus === 1" class="px-2 py-0.5 text-[11px] font-semibold bg-green-100 text-green-700 rounded border border-green-200">Submitted</span>
            <span v-else class="px-2 py-0.5 text-[11px] font-semibold bg-yellow-100 text-yellow-700 rounded border border-yellow-200">Draft</span>
          </div>
          <div class="flex items-center gap-2">
            <span v-if="formLoading" class="lucide-loader-2 size-4 text-gray-400 animate-spin" />
            <button @click="showForm = false" class="text-gray-400 hover:text-gray-600 transition text-lg leading-none px-1">✕</button>
          </div>
        </div>

        <!-- Scrollable form body -->
        <div class="flex-1 overflow-y-auto bg-white">

          <!-- Section: Details -->
          <div class="px-4 py-2 bg-gray-50 border-b border-gray-200 shrink-0">
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Details</span>
          </div>

          <div class="px-6 py-4 grid grid-cols-2 gap-x-8 gap-y-4 border-b border-gray-100">
            <!-- Supplier field -->
            <div class="col-span-2">
              <label class="block text-xs text-gray-500 mb-1">Supplier <span class="text-red-500">*</span></label>

              <!-- Selected state -->
              <div v-if="selectedSupplier" class="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded bg-white">
                <span class="text-sm text-gray-800 flex-1">{{ selectedSupplier.supplier_name }}</span>
                <span class="text-xs text-gray-400 border-l border-gray-200 pl-2">{{ selectedSupplier.supplier_type }}</span>
                <button
                  v-if="formDocstatus !== 1"
                  @click="selectedSupplier = null; supplierSearchInput = ''; isSupplierDropdownOpen = true"
                  class="text-xs text-blue-600 hover:text-blue-800 border-l border-gray-200 pl-2 ml-1"
                >Change</button>
              </div>

              <!-- Search state -->
              <div v-else class="relative">
                <input
                  v-model="supplierSearchInput"
                  @focus="isSupplierDropdownOpen = true"
                  @input="fetchSuppliers"
                  @keydown.esc="isSupplierDropdownOpen = false"
                  type="text"
                  placeholder="Search Supplier"
                  class="w-full border border-gray-300 rounded px-3 py-1.5 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400/30 bg-white"
                />
                <div v-if="isSupplierDropdownOpen && filteredSuppliers.length > 0"
                  class="absolute left-0 right-0 top-full mt-0.5 bg-white border border-gray-200 rounded shadow-lg max-h-48 overflow-y-auto z-50">
                  <div v-for="s in filteredSuppliers" :key="s.name" @click="selectSupplier(s)"
                    class="px-3 py-2 hover:bg-blue-50 cursor-pointer text-sm flex items-center justify-between">
                    <span class="text-gray-800">{{ s.supplier_name }}</span>
                    <span class="text-xs text-gray-400">{{ s.supplier_type }}</span>
                  </div>
                  <div class="px-3 py-2 border-t border-gray-100">
                    <button @click="openAddSupplier" class="text-xs text-blue-600 hover:underline flex items-center gap-1">
                      <span class="lucide-plus size-3" />Create New Supplier
                    </button>
                  </div>
                </div>
                <div v-if="isSupplierDropdownOpen && supplierSearchInput && filteredSuppliers.length === 0 && !suppliersLoading"
                  class="absolute left-0 right-0 top-full mt-0.5 bg-white border border-gray-200 rounded shadow-lg z-50">
                  <div class="px-3 py-2 text-xs text-gray-400">No supplier found</div>
                  <div class="px-3 py-2 border-t border-gray-100">
                    <button @click="openAddSupplier" class="text-xs text-blue-600 hover:underline flex items-center gap-1">
                      <span class="lucide-plus size-3" />Create "{{ supplierSearchInput }}"
                    </button>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- Section: Items (child table) -->
          <div class="px-4 py-2 bg-gray-50 border-b border-gray-200 flex items-center justify-between">
            <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Items</span>
            <span class="text-xs text-gray-400">{{ purchaseItems.length }} row(s)</span>
          </div>

          <!-- Child table -->
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-200">
                <th class="w-8 py-2 px-2 text-center text-xs font-medium text-gray-400 border-r border-gray-200">#</th>
                <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 border-r border-gray-200">Item</th>
                <th class="w-28 py-2 px-3 text-left text-xs font-medium text-gray-500 border-r border-gray-200">Qty</th>
                <th class="w-32 py-2 px-3 text-left text-xs font-medium text-gray-500 border-r border-gray-200">Rate (₹)</th>
                <th class="w-32 py-2 px-3 text-left text-xs font-medium text-gray-500 border-r border-gray-200">Amount</th>
                <th class="w-8 py-2 px-2"></th>
              </tr>
            </thead>
            <tbody>
              <!-- Rows -->
              <tr
                v-for="(row, idx) in purchaseItems"
                :key="idx"
                class="border-b border-gray-100 hover:bg-gray-50 group"
              >
                <td class="py-1.5 px-2 text-center text-xs text-gray-400 border-r border-gray-200">{{ idx + 1 }}</td>
                <td class="py-1 px-2 border-r border-gray-200 relative">
                  <!-- View mode: plain text -->
                  <template v-if="formDocstatus === 1">
                    <div class="text-sm text-gray-800 py-0.5">{{ row.item_name || row.item_code }}</div>
                    <div class="text-xs text-gray-400">{{ row.item_code }}</div>
                  </template>
                  <!-- Edit mode: inline link search -->
                  <template v-else>
                    <input
                      v-model="row._search"
                      @focus="activeItemRowIdx = idx"
                      @keydown.esc="activeItemRowIdx = -1"
                      type="text"
                      placeholder="Search item..."
                      class="w-full border border-gray-300 rounded px-2 py-1 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400/30 bg-white"
                    />
                    <div
                      v-if="activeItemRowIdx === idx && filteredRowItems(row._search).length > 0"
                      class="absolute left-0 right-0 top-full mt-0.5 bg-white border border-gray-200 rounded shadow-xl max-h-48 overflow-y-auto z-50"
                    >
                      <div
                        v-for="item in filteredRowItems(row._search)"
                        :key="item.item_code"
                        @mousedown.prevent="selectItemForRow(idx, item)"
                        class="px-3 py-2 hover:bg-blue-50 cursor-pointer text-sm border-b border-gray-50 last:border-0"
                      >
                        <div class="text-gray-800 font-medium">{{ item.item_name || item.item_code }}</div>
                        <div class="text-xs text-gray-400">{{ item.item_code }} · {{ item.stock_uom }}</div>
                      </div>
                    </div>
                  </template>
                </td>
                <td class="py-1 px-2 border-r border-gray-200">
                  <input
                    v-if="formDocstatus !== 1"
                    type="number" min="0.01" step="0.01"
                    v-model.number="row.qty"
                    class="w-full border border-gray-300 rounded px-2 py-1 text-sm text-gray-800 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400/30"
                  />
                  <span v-else class="text-sm text-gray-700 px-1">{{ row.qty }}</span>
                </td>
                <td class="py-1 px-2 border-r border-gray-200">
                  <input
                    v-if="formDocstatus !== 1"
                    type="number" min="0" step="0.01"
                    v-model.number="row.rate"
                    class="w-full border border-gray-300 rounded px-2 py-1 text-sm text-gray-800 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400/30"
                  />
                  <span v-else class="text-sm text-gray-700 px-1">{{ row.rate }}</span>
                </td>
                <td class="py-1.5 px-3 text-sm text-gray-700 border-r border-gray-200">
                  {{ (row.qty * row.rate).toFixed(2) }}
                </td>
                <td class="py-1.5 px-2 text-center">
                  <button
                    v-if="formDocstatus !== 1"
                    @click="purchaseItems.splice(idx, 1)"
                    class="text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition"
                  ><span class="lucide-x size-3.5" /></button>
                </td>
              </tr>

              <!-- Add Row button row (only in new/draft mode) -->
              <tr v-if="formDocstatus !== 1" class="border-b border-gray-100">
                <td colspan="6" class="py-2 px-3">
                  <button
                    @click="addEmptyRow"
                    class="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1"
                  ><span class="lucide-plus size-3.5" />Add Row</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Totals (Frappe style, right-aligned) -->
          <div v-if="purchaseItems.length" class="flex justify-end px-4 py-2 border-t border-gray-200 bg-gray-50">
            <table class="text-sm">
              <tr>
                <td class="py-0.5 pr-8 text-gray-500 text-right">Total Qty</td>
                <td class="py-0.5 pl-4 text-gray-800 font-medium text-right w-28">{{ totalPurchaseQty.toFixed(3) }}</td>
              </tr>
              <tr>
                <td class="py-0.5 pr-8 text-gray-500 text-right">Total Amount</td>
                <td class="py-0.5 pl-4 text-gray-900 font-semibold text-right w-28">₹ {{ totalPurchaseAmount.toFixed(2) }}</td>
              </tr>
            </table>
          </div>
        </div>

        <!-- Frappe-style footer toolbar -->
        <div class="px-4 py-3 border-t border-gray-200 bg-gray-50 flex items-center justify-between shrink-0 rounded-b-lg">
          <div class="text-xs text-gray-400">
            <span v-if="formDocstatus !== 1 && !formEntryName && !selectedSupplier" class="text-orange-500">⚠ Select Supplier to continue</span>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="showForm = false"
              class="px-4 py-1.5 text-sm text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition"
            >{{ formDocstatus === 1 ? 'Close' : 'Discard' }}</button>

            <!-- New entry: Save as Draft -->
            <button
              v-if="!formEntryName"
              @click="saveDraft"
              :disabled="!selectedSupplier || isSubmitting"
              class="px-5 py-1.5 text-sm font-medium text-gray-800 bg-white hover:bg-gray-50 border border-gray-400 rounded disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-1.5"
            >
              <span v-if="isSubmitting" class="lucide-loader-2 size-3.5 animate-spin" />
              {{ isSubmitting ? 'Saving...' : 'Save as Draft' }}
            </button>

            <!-- Draft entry: Submit button -->
            <button
              v-if="formEntryName && formDocstatus === 0"
              @click="submitEntry"
              :disabled="isSubmitting"
              class="px-5 py-1.5 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 border border-blue-600 rounded disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-1.5"
            >
              <span v-if="isSubmitting" class="lucide-loader-2 size-3.5 animate-spin" />
              {{ isSubmitting ? 'Submitting...' : 'Submit' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add New Supplier Popup -->
    <div
      v-if="showAddSupplier"
      class="fixed inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center z-[60] p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <div class="flex items-center justify-between border-b border-gray-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="lucide-building-2 size-4 text-emerald-600" />
            <h3 class="text-sm font-bold text-gray-900">Add New Supplier</h3>
          </div>
          <button @click="showAddSupplier = false" class="text-gray-400 hover:text-gray-600 text-sm">✕</button>
        </div>

        <div class="space-y-3">
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Supplier / Company Name *</label>
            <input
              v-model="newSupplierName"
              type="text"
              placeholder="e.g. Raymond Fabrics, Siyaram Mills"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Type</label>
            <select
              v-model="newSupplierType"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="Company">Company</option>
              <option value="Individual">Individual</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-1">
          <button
            @click="showAddSupplier = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >Cancel</button>
          <button
            @click="submitAddSupplier"
            :disabled="!newSupplierName.trim() || isSubmittingSupplier"
            class="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm disabled:opacity-50"
          >
            <span v-if="isSubmittingSupplier">Saving...</span>
            <span v-else>Save Supplier</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  entries: { type: Array, default: () => [] },
  items: { type: Array, default: () => [] },
});

const emit = defineEmits(['refresh']);

// Form state
const showForm = ref(false);
const formLoading = ref(false);
const isSubmitting = ref(false);
const formEntryName = ref('');
const formDocstatus = ref(0);

// Supplier
const selectedSupplier = ref(null);
const supplierSearchInput = ref('');
const isSupplierDropdownOpen = ref(false);
const suppliers = ref([]);
const suppliersLoading = ref(false);

// Items — each row has _search (link input text) and _open (dropdown open)
const purchaseItems = ref([]);
const activeItemRowIdx = ref(-1);

// Add supplier popup
const showAddSupplier = ref(false);
const newSupplierName = ref('');
const newSupplierType = ref('Company');
const isSubmittingSupplier = ref(false);

function formatDate(date) {
  if (!date) return '—';
  const [y, m, d] = String(date).split('-');
  return `${d}-${m}-${y}`;
}

function makeRow(overrides = {}) {
  return { item_code: '', item_name: '', qty: 1, rate: 0, uom: 'Nos', _search: '', ...overrides };
}

function openForm() {
  formEntryName.value = '';
  formDocstatus.value = 0;
  selectedSupplier.value = null;
  supplierSearchInput.value = '';
  purchaseItems.value = [makeRow()];
  activeItemRowIdx.value = -1;
  isSupplierDropdownOpen.value = false;
  showForm.value = true;
  fetchSuppliers();
}

async function openDetail(name) {
  formLoading.value = true;
  formEntryName.value = name;
  formDocstatus.value = 0;
  selectedSupplier.value = null;
  purchaseItems.value = [];
  activeItemRowIdx.value = -1;
  showForm.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_purchase_entry_detail', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ entry_name: name }),
    });
    const json = await res.json();
    const d = json.message;
    if (d) {
      formDocstatus.value = d.docstatus;
      selectedSupplier.value = d.supplier
        ? { name: d.supplier, supplier_name: d.supplier_name || d.supplier, supplier_type: '' }
        : null;
      purchaseItems.value = (d.items || []).map((r) =>
        makeRow({ item_code: r.item_code, item_name: r.item_name || r.item_code, qty: r.qty, rate: r.basic_rate || 0, uom: r.uom || 'Nos', _search: r.item_name || r.item_code })
      );
    }
  } catch {}
  formLoading.value = false;
}

async function fetchSuppliers() {
  suppliersLoading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_suppliers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ query: supplierSearchInput.value }),
    });
    const json = await res.json();
    suppliers.value = json.message || [];
  } catch {
    suppliers.value = [];
  } finally {
    suppliersLoading.value = false;
  }
}

const filteredSuppliers = computed(() => {
  if (!supplierSearchInput.value) return suppliers.value;
  const q = supplierSearchInput.value.toLowerCase();
  return suppliers.value.filter(
    (s) => s.supplier_name.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)
  );
});

function selectSupplier(s) {
  selectedSupplier.value = s;
  isSupplierDropdownOpen.value = false;
  supplierSearchInput.value = '';
}

function filteredRowItems(search) {
  if (!search) return props.items.slice(0, 20);
  const q = search.toLowerCase();
  return props.items
    .filter(
      (i) =>
        (i.item_name && i.item_name.toLowerCase().includes(q)) ||
        (i.item_code && i.item_code.toLowerCase().includes(q))
    )
    .slice(0, 20);
}

function selectItemForRow(idx, item) {
  const row = purchaseItems.value[idx];
  row.item_code = item.item_code;
  row.item_name = item.item_name || item.item_code;
  row.uom = item.stock_uom || 'Nos';
  row._search = item.item_name || item.item_code;
  activeItemRowIdx.value = -1;
}

function addEmptyRow() {
  purchaseItems.value.push(makeRow());
  activeItemRowIdx.value = purchaseItems.value.length - 1;
}

const totalPurchaseAmount = computed(() =>
  purchaseItems.value.reduce((s, r) => s + r.qty * r.rate, 0)
);

const totalPurchaseQty = computed(() =>
  purchaseItems.value.reduce((s, r) => s + r.qty, 0)
);

function openAddSupplier() {
  newSupplierName.value = supplierSearchInput.value;
  newSupplierType.value = 'Company';
  showAddSupplier.value = true;
  isSupplierDropdownOpen.value = false;
}

async function submitAddSupplier() {
  if (!newSupplierName.value.trim()) return;
  isSubmittingSupplier.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.create_supplier', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ supplier_name: newSupplierName.value.trim(), supplier_type: newSupplierType.value }),
    });
    const json = await res.json();
    if (json.message) {
      suppliers.value.unshift(json.message);
      selectedSupplier.value = json.message;
      showAddSupplier.value = false;
      newSupplierName.value = '';
    } else {
      alert('Error: ' + JSON.stringify(json._server_messages || json));
    }
  } catch {
    alert('Failed to create supplier');
  } finally {
    isSubmittingSupplier.value = false;
  }
}

function parseFrappeError(json) {
  try {
    if (json._server_messages) {
      const msgs = JSON.parse(json._server_messages);
      return msgs.map((m) => { try { return JSON.parse(m).message; } catch { return m; } }).join('\n');
    }
    if (json.exc) return json.exc.split('\n').filter(Boolean).slice(-3).join('\n');
  } catch {}
  return JSON.stringify(json);
}

async function saveDraft() {
  if (!selectedSupplier.value) { alert('Select a supplier first'); return; }
  const validItems = purchaseItems.value.filter((r) => r.item_code && r.qty > 0);
  if (validItems.length === 0) { alert('Add at least one valid item'); return; }
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.save_purchase_draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({
        supplier: selectedSupplier.value.name,
        items: validItems.map((r) => ({ item_code: r.item_code, qty: r.qty, rate: r.rate })),
      }),
    });
    const json = await res.json();
    if (json.message && json.message.name) {
      emit('refresh');
      await openDetail(json.message.name);
    } else {
      alert('Error:\n' + parseFrappeError(json));
    }
  } catch {
    alert('Network error while saving draft');
  } finally {
    isSubmitting.value = false;
  }
}

async function submitEntry() {
  if (!formEntryName.value) return;
  const ok = confirm(`Submit ${formEntryName.value}?\n\nOnce submitted, stock will be updated and entry cannot be edited.`);
  if (!ok) return;
  isSubmitting.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.submit_stock_entry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ entry_name: formEntryName.value }),
    });
    const json = await res.json();
    if (json.message && json.message.docstatus === 1) {
      formDocstatus.value = 1;
      emit('refresh');
    } else {
      alert('Error:\n' + parseFrappeError(json));
    }
  } catch {
    alert('Network error while submitting');
  } finally {
    isSubmitting.value = false;
  }
}
</script>
