<template>
  <div class="h-screen w-screen flex bg-gray-50 overflow-hidden font-sans select-none">
    <!-- Left Compact Icon-Style Sidebar (Light Theme, Collapsed with Visible Labels) -->
    <aside class="w-16 bg-white border-r border-gray-200 flex flex-col justify-between items-center py-3 flex-shrink-0 z-30 shadow-xs">
      <div class="flex flex-col items-center gap-4 w-full">
        <!-- Brand Icon -->
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-xs">
          <span class="lucide-scissors size-5 text-white" />
        </div>

        <!-- Navigation Links (Vertical Icon + Label Badge) -->
        <nav class="flex flex-col items-center gap-2 w-full px-1">
          <!-- 1. POS -->
          <button
            @click="currentTab = 'pos'"
            :class="currentTab === 'pos' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Point of Sale"
          >
            <span class="lucide-shopping-cart size-5" />
            <span class="text-[10px] mt-1 leading-tight tracking-tight">POS</span>
          </button>

          <!-- 2. Invoices -->
          <button
            @click="switchTab('invoices')"
            :class="currentTab === 'invoices' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Sales Invoices"
          >
            <span class="lucide-receipt size-5" />
            <span class="text-[10px] mt-1 leading-tight tracking-tight">Invoices</span>
          </button>

          <!-- 3. Purchase Entry -->
          <button
            @click="switchTab('stock')"
            :class="currentTab === 'stock' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Purchase Entries"
          >
            <span class="lucide-package size-5" />
            <span class="text-[9.5px] mt-1 leading-tight tracking-tight">Purchase</span>
          </button>
        </nav>
      </div>

      <!-- Bottom Desk Link -->
      <div class="w-full px-1 flex flex-col items-center">
        <button
          @click="goToDesk"
          class="w-full flex flex-col items-center justify-center py-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-xl transition"
          title="Go to Desk"
        >
          <span class="lucide-external-link size-4" />
          <span class="text-[9px] mt-1">Desk</span>
        </button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Left Main Body (No top header for POS, full space) -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top Header Bar (Items management only; Purchase/Invoices have their own headers) -->
        <header
          v-if="currentTab === 'items'"
          class="bg-white border-b border-gray-200 px-4 py-2.5 flex items-center justify-between shadow-2xs z-20 shrink-0"
        >
          <div class="flex items-center gap-3">
            <h2 class="text-base font-bold text-gray-900">Item Catalogue</h2>
            <span class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-md">Live</span>
          </div>
        </header>

        <!-- View 1: POS Screen Left Column -->
        <div v-show="currentTab === 'pos'" class="flex-1 flex overflow-hidden">
        <section class="flex-1 flex flex-col bg-gray-50 overflow-hidden border-r border-gray-200">
        <!-- Brand Items Capsule Bar -->
        <div class="px-3.5 py-2.5 bg-white border-b border-gray-200 flex items-center gap-2 overflow-x-auto scrollbar-none">
          <!-- + Brand Button before All Brands -->
          <button
            @click="showCreateTemplateModal = true"
            class="px-3 py-1.5 rounded-[11px] text-xs font-bold bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 transition shadow-2xs flex items-center gap-1 shrink-0 whitespace-nowrap"
            title="Create Brand"
          >
            <span class="lucide-plus size-3.5" />
            <span>Brand</span>
          </button>

          <button
            @click="selectedTemplate = ''"
            :class="!selectedTemplate ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
            class="px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition shadow-xs"
          >
            All Brands
          </button>
          <button
            v-for="tmpl in templates"
            :key="tmpl.item_code"
            @click="selectedTemplate = tmpl.item_code"
            :class="selectedTemplate === tmpl.item_code ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
            class="px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition shadow-xs"
          >
            {{ tmpl.item_name || tmpl.item_code }}
          </button>
        </div>

        <!-- Search Bar with Instant Filter -->
        <div class="p-3 bg-white border-b border-gray-200">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by item code, name or barcode..."
              class="w-full bg-gray-50 border border-gray-200 rounded-xl pl-10 pr-8 py-2.5 text-sm focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
            />
            <span class="absolute left-3.5 top-3 text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-3.5 top-2.5 text-gray-400 hover:text-gray-600 text-sm"
            >✕</button>
          </div>
        </div>

        <!-- Items Grid Cards (Dense, Compact Tiles with 14px Readable Standard Font) -->
        <div class="flex-1 overflow-y-auto p-3 content-start grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2.5">
          <!-- First Card: Always + Add Item Card -->
          <button
            @click="openVariantModal(selectedTemplate)"
            class="group relative rounded-xl p-2.5 h-20 self-start flex flex-col items-center justify-center border-2 border-dashed border-gray-300 hover:border-emerald-500 bg-white hover:bg-emerald-50/40 transition-all text-gray-400 hover:text-emerald-700 shadow-2xs cursor-pointer active:scale-[0.98]"
            title="Add New Item"
          >
            <div class="w-7 h-7 rounded-full bg-emerald-50 group-hover:bg-emerald-100 flex items-center justify-center text-emerald-600 transition">
              <span class="lucide-plus size-4" />
            </div>
            <span class="text-xs font-bold mt-1 text-gray-700 group-hover:text-emerald-700">Add Item</span>
          </button>

          <div
            v-for="item in filteredItems"
            :key="item.item_code"
            @click="addToCart(item)"
            :class="[
              'group relative rounded-xl p-2.5 touch-manipulation transition-all duration-100 h-20 self-start flex flex-col justify-between shadow-xs',
              item.is_stock_item && Number(item.actual_qty || 0) <= 0
                ? 'bg-gray-100/80 border border-gray-200 opacity-60 cursor-not-allowed'
                : 'bg-white border border-gray-200 hover:border-blue-500 hover:shadow-sm cursor-pointer active:scale-[0.98]'
            ]"
          >
            <!-- Available Qty Badge (POS Next style: overlapping pill badge at top-right) -->
            <div
              v-if="item.is_stock_item"
              :class="[
                'absolute -top-2.5 -right-2 z-20 px-2.5 py-0.5 rounded-full text-xs font-black text-white shadow-xs select-none leading-none tracking-tight flex items-center justify-center min-w-[28px] h-5',
                Number(item.actual_qty || 0) <= 0 ? 'bg-[#ef4444]' : 'bg-[#22c55e]'
              ]"
              :title="Number(item.actual_qty || 0) <= 0 ? 'Out of stock' : `Available Stock: ${item.actual_qty ?? 0}`"
            >
              {{ Math.floor(item.actual_qty ?? 0) }}
            </div>

            <!-- Cart Count Badge (top-left inside card) -->
            <div
              v-if="getItemCartQty(item.item_code)"
              class="absolute -top-1.5 -left-1.5 rounded-[11px] shadow-xs z-10 px-1.5 h-5 min-w-[20px] flex items-center justify-center text-[10px] font-bold border border-white bg-blue-600 text-white select-none"
            >
              {{ getItemCartQty(item.item_code) }}
            </div>

            <!-- Item Header -->
            <div class="min-w-0 pr-6">
              <h3
                class="text-sm font-bold text-gray-900 group-hover:text-blue-600 transition leading-snug truncate"
                :title="item.item_name || item.item_code"
              >
                {{ item.item_name || item.item_code }}
              </h3>
              <p class="text-xs text-gray-500 font-mono leading-tight truncate">
                {{ item.item_code }}
              </p>
            </div>

            <!-- Bottom Price & UOM -->
            <div class="pt-1 border-t border-gray-100 flex items-center justify-between text-xs leading-tight">
              <div v-if="item.selling_price != null" class="flex items-baseline gap-1">
                <span class="font-extrabold text-blue-600 text-sm">
                  ₹{{ Number(item.selling_price).toFixed(2) }}
                </span>
                <span class="text-gray-500 text-xs">/ {{ item.stock_uom || 'Nos' }}</span>
              </div>
              <span v-else class="text-xs text-amber-600 font-semibold bg-amber-50 px-1 py-0.5 rounded border border-amber-200">No price</span>

              <!-- Edit Price Button -->
              <button
                @click.stop="openPriceEditModal(item)"
                class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition"
                title="Edit / Set Selling Price"
              >
                <span class="lucide-pencil size-3.5" />
              </button>
            </div>
          </div>

          <div v-if="filteredItems.length === 0" class="col-span-full h-48 flex flex-col items-center justify-center text-gray-400 text-sm">
            No items matching your search criteria
          </div>
        </div>
      </section>

      <!-- Right Column: Shopping Cart (Full Height Screen Layout for POS) -->
      <aside class="w-[380px] bg-white flex flex-col shadow-xl z-20 border-l border-gray-200 h-full flex-shrink-0">
        <!-- Customer Selection Card (Matching Brand Bar Height & Frappe UI Lucide Icons) -->
        <div class="px-3.5 py-2.5 border-b border-gray-200 bg-white relative flex items-center min-h-[49px]">
          <!-- Selected Customer Card -->
          <div v-if="selectedCustomerDoc" class="flex items-center justify-between w-full">
            <div class="flex items-center gap-2 min-w-0 flex-1">
              <div class="w-7 h-7 rounded-[11px] bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 border border-blue-200">
                <span class="lucide-user size-4" />
              </div>
              <div class="min-w-0 flex-1 leading-tight">
                <div class="text-sm font-bold text-gray-900 truncate">
                  {{ selectedCustomerDoc.customer_name }}
                </div>
                <div class="text-[11px] text-gray-500 truncate flex items-center gap-1">
                  <span v-if="selectedCustomerDoc.mobile_no" class="text-blue-600 font-medium">{{ selectedCustomerDoc.mobile_no }}</span>
                  <span v-else class="text-gray-400">Walk-in</span>
                </div>
              </div>
            </div>

            <!-- Change Customer Button -->
            <button
              @click="toggleCustomerSearch"
              class="px-2.5 py-1 text-xs text-blue-600 hover:bg-blue-50 rounded-[11px] font-semibold transition shrink-0 ml-2 border border-blue-200/70"
            >
              Change
            </button>
          </div>

          <!-- Customer Live Search Field -->
          <div v-else ref="customerSearchContainer" class="relative w-full">
            <div class="relative flex items-center">
              <span class="absolute left-2.5 text-gray-400 flex items-center pointer-events-none">
                <span class="lucide-user size-4" />
              </span>
              <input
                v-model="customerSearchInput"
                @focus="isCustomerDropdownOpen = true"
                @keydown.esc="isCustomerDropdownOpen = false"
                type="text"
                placeholder="Search customer by name or phone..."
                class="w-full bg-gray-50 border border-gray-200 rounded-[11px] pl-8 pr-16 py-1.5 text-xs font-medium text-gray-800 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition h-8"
              />
              <button
                @click="showAddCustomer = true"
                class="absolute right-1.5 px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg transition shadow-2xs h-6 flex items-center gap-1"
              >
                <span class="lucide-plus size-3 text-white" />
                <span class="text-white">New</span>
              </button>
            </div>

            <!-- Dropdown Results -->
            <div
              v-if="isCustomerDropdownOpen"
              class="absolute left-0 right-0 top-full mt-1 bg-white border border-gray-200 rounded-[11px] shadow-xl max-h-56 overflow-y-auto z-40 divide-y divide-gray-100"
            >
              <div
                v-for="c in searchedCustomers"
                :key="c.name"
                @click="selectCustomer(c)"
                class="p-2.5 hover:bg-blue-50/70 cursor-pointer transition flex items-center justify-between"
              >
                <div class="min-w-0 flex-1 pr-2">
                  <div class="text-sm font-bold text-gray-900 truncate">{{ c.customer_name || c.name }}</div>
                  <div class="text-xs text-gray-500 truncate flex items-center gap-2 mt-0.5">
                    <span v-if="c.mobile_no" class="text-blue-600 font-medium">📞 {{ c.mobile_no }}</span>
                    <span class="text-gray-400">{{ c.name }}</span>
                  </div>
                </div>
                <span class="text-xs text-blue-500 font-semibold">Select →</span>
              </div>

              <div v-if="searchedCustomers.length === 0" class="p-3 text-center text-xs text-gray-400">
                No customer found. Click <b>+ New</b> to create.
              </div>
            </div>
          </div>
        </div>

        <!-- Cart Items List -->
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div v-if="cart.length === 0" class="h-full flex flex-col items-center justify-center text-gray-400">
            <div class="w-14 h-14 rounded-2xl bg-gray-100 flex items-center justify-center mb-2.5 text-gray-400 border border-gray-200">
              <span class="lucide-shopping-cart size-6 text-gray-400" />
            </div>
            <span class="text-sm font-bold text-gray-600">Cart is empty</span>
            <span class="text-xs text-gray-400 mt-0.5">Click any item from catalogue</span>
          </div>

          <div
            v-for="(row, idx) in cart"
            :key="idx"
            class="p-2.5 border border-gray-200 rounded-xl bg-gray-50/60 hover:bg-gray-50 flex items-center justify-between transition"
          >
            <div class="flex-1 min-w-0 pr-2">
              <div class="text-sm font-bold text-gray-900 truncate">{{ row.item_name }}</div>
              <div class="text-xs text-gray-500 mt-0.5">
                ₹{{ row.rate.toFixed(2) }} × {{ row.qty }} = <b class="text-gray-900 font-extrabold text-sm">₹{{ (row.rate * row.qty).toFixed(2) }}</b>
              </div>
            </div>

            <!-- Qty Stepper & Input Controls -->
            <div class="flex items-center bg-white border border-gray-300 rounded-[11px] p-0.5 shadow-xs">
              <button
                @click.stop="decreaseQty(idx)"
                class="w-7 h-7 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded-[11px] text-sm font-bold"
              >-</button>
              <input
                type="number"
                step="0.01"
                min="0.01"
                :value="row.qty"
                @click.stop
                @change="updateCartRowQty(idx, $event.target.value)"
                class="w-14 text-center font-extrabold text-sm text-gray-900 bg-transparent border-0 outline-none focus:outline-none focus:ring-0 p-0 shadow-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <button
                @click.stop="increaseQty(idx)"
                class="w-7 h-7 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded-[11px] text-sm font-bold"
              >+</button>
            </div>
          </div>
        </div>

        <!-- Totals & Payment Section -->
        <div class="p-4 border-t border-gray-200 bg-gray-50 space-y-3">
          <!-- Quick Mode of Payment Tabs (Cash, UPI, Split) -->
          <div>
            <div class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5 flex items-center justify-between">
              <span>Payment Method</span>
              <span v-if="selectedPaymentMode === 'Split'" class="text-[11px] font-semibold text-blue-600 lowercase">
                cash + upi
              </span>
            </div>
            <div class="grid grid-cols-3 gap-1.5">
              <button
                @click="setPaymentMode('Cash')"
                :class="selectedPaymentMode === 'Cash' ? 'border-blue-600 bg-blue-50 text-blue-700 font-bold shadow-xs ring-1 ring-blue-500/20' : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-100'"
                class="px-2 py-2 border rounded-lg text-xs font-medium text-center transition flex items-center justify-center gap-1"
              >
                <span class="lucide-banknote size-3.5" />
                <span>Cash</span>
              </button>
              <button
                @click="setPaymentMode('UPI')"
                :class="selectedPaymentMode === 'UPI' ? 'border-blue-600 bg-blue-50 text-blue-700 font-bold shadow-xs ring-1 ring-blue-500/20' : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-100'"
                class="px-2 py-2 border rounded-lg text-xs font-medium text-center transition flex items-center justify-center gap-1"
              >
                <span class="lucide-qr-code size-3.5" />
                <span>UPI</span>
              </button>
              <button
                @click="setPaymentMode('Split')"
                :class="selectedPaymentMode === 'Split' ? 'border-blue-600 bg-blue-50 text-blue-700 font-bold shadow-xs ring-1 ring-blue-500/20' : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-100'"
                class="px-2 py-2 border rounded-lg text-xs font-medium text-center transition flex items-center justify-center gap-1"
              >
                <span class="lucide-split size-3.5" />
                <span>Split</span>
              </button>
            </div>

            <!-- Split Payment Breakdown Inputs -->
            <div v-if="selectedPaymentMode === 'Split'" class="mt-2.5 p-2.5 bg-white border border-blue-200 rounded-xl space-y-2 shadow-2xs">
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-[11px] font-bold text-gray-600 mb-1 flex items-center gap-1">
                    <span class="lucide-banknote size-3 text-emerald-600" />
                    <span>Cash Amount</span>
                  </label>
                  <div class="relative">
                    <span class="absolute left-2.5 top-2 text-xs text-gray-400 font-bold">₹</span>
                    <input
                      type="number"
                      min="0"
                      step="any"
                      :max="subtotal"
                      v-model.number="splitCashAmount"
                      @input="onSplitCashChange"
                      class="w-full bg-gray-50 border border-gray-200 rounded-lg pl-6 pr-2 py-1.5 text-xs font-bold text-gray-900 focus:outline-none focus:bg-white focus:border-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-[11px] font-bold text-gray-600 mb-1 flex items-center gap-1">
                    <span class="lucide-qr-code size-3 text-blue-600" />
                    <span>UPI Amount</span>
                  </label>
                  <div class="relative">
                    <span class="absolute left-2.5 top-2 text-xs text-gray-400 font-bold">₹</span>
                    <input
                      type="number"
                      min="0"
                      step="any"
                      :max="subtotal"
                      v-model.number="splitUpiAmount"
                      @input="onSplitUpiChange"
                      class="w-full bg-gray-50 border border-gray-200 rounded-lg pl-6 pr-2 py-1.5 text-xs font-bold text-gray-900 focus:outline-none focus:bg-white focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>

              <!-- Split Balance Indicator -->
              <div class="flex items-center justify-between text-[11px] font-medium pt-1 border-t border-gray-100">
                <span class="text-gray-500">Allocated: ₹{{ (Number(splitCashAmount || 0) + Number(splitUpiAmount || 0)).toFixed(2) }}</span>
                <span
                  :class="splitDifference === 0 ? 'text-emerald-600 font-bold' : 'text-amber-600 font-bold'"
                >
                  {{ splitDifference === 0 ? '✓ Balanced' : `Diff: ₹${splitDifference.toFixed(2)}` }}
                </span>
              </div>
            </div>
          </div>

          <!-- Totals Breakdown -->
          <div class="border-t border-gray-200 pt-2.5 space-y-1">
            <div class="flex justify-between text-sm text-gray-500 font-medium">
              <span>Items Total ({{ totalQuantity }}):</span>
              <span>₹{{ subtotal.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-base font-extrabold text-gray-900 pt-1 border-t border-dashed border-gray-200">
              <span>Grand Total:</span>
              <span class="text-blue-600 text-lg">₹{{ subtotal.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Checkout Button -->
          <button
            @click="createInvoice"
            :disabled="cart.length === 0 || isSubmitting"
            class="w-full py-3 rounded-xl text-white font-extrabold text-sm bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed shadow-md transition flex items-center justify-center gap-2 active:scale-[0.99]"
          >
            <span v-if="isSubmitting">Generating Invoice...</span>
            <span v-else>Pay & Print (₹{{ subtotal.toFixed(2) }})</span>
          </button>
        </div>
      </aside>
      </div>

      <!-- View 1.5: Items Management Screen (Exact POS Cards Layout + Brand & Item Creator) -->
      <div v-show="currentTab === 'items'" class="flex-1 flex flex-col bg-gray-50 overflow-hidden">
        <!-- Top Toolbar & Brands Filter Bar -->
        <div class="px-4 py-2.5 bg-white border-b border-gray-200 flex items-center justify-between gap-3">
          <div class="flex items-center gap-2 overflow-x-auto scrollbar-none flex-1">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider flex-shrink-0">Brands:</span>
            <button
              @click="itemsTabSelectedTemplate = ''"
              :class="!itemsTabSelectedTemplate ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition shadow-xs"
            >
              All ({{ items.length }})
            </button>
            <button
              v-for="tmpl in templates"
              :key="tmpl.item_code"
              @click="itemsTabSelectedTemplate = tmpl.item_code"
              :class="itemsTabSelectedTemplate === tmpl.item_code ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition shadow-xs flex items-center gap-1.5"
            >
              <span>{{ tmpl.item_name || tmpl.item_code }}</span>
            </button>
          </div>

          <!-- Live Filter Input -->
          <div class="w-64 relative flex-shrink-0">
            <input
              v-model="itemsSearchQuery"
              type="text"
              placeholder="Search items..."
              class="w-full bg-gray-50 border border-gray-200 rounded-xl pl-8 pr-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <span class="absolute left-2.5 top-2 text-gray-400 text-xs">🔍</span>
          </div>
        </div>

        <!-- Items Cards Grid (Same Compact & Readable Cards) -->
        <div class="flex-1 overflow-y-auto p-4 content-start grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
          <!-- First Card: Always + Add Item Card in Items Tab -->
          <button
            @click="openVariantModal(itemsTabSelectedTemplate)"
            class="group relative bg-white border-2 border-dashed border-gray-300 hover:border-emerald-500 rounded-xl p-2.5 transition-all shadow-2xs hover:bg-emerald-50/40 flex flex-col items-center justify-center h-24 self-start cursor-pointer active:scale-[0.98]"
            title="Add New Item"
          >
            <div class="w-8 h-8 rounded-full bg-emerald-50 group-hover:bg-emerald-100 flex items-center justify-center text-emerald-600 transition">
              <span class="lucide-plus size-4" />
            </div>
            <span class="text-xs font-bold mt-1.5 text-gray-700 group-hover:text-emerald-700">Add Item</span>
          </button>

          <div
            v-for="item in itemsTabFilteredList"
            :key="item.item_code"
            class="group relative bg-white border border-gray-200 hover:border-blue-500 rounded-xl p-2.5 transition-all shadow-xs hover:shadow-sm flex flex-col justify-between h-24 self-start"
          >
            <!-- Available Stock Badge (POS Next style: overlapping pill badge at top-right) -->
            <div
              v-if="item.is_stock_item"
              :class="[
                'absolute -top-2.5 -right-2 z-20 px-2.5 py-0.5 rounded-full text-xs font-black text-white shadow-xs select-none leading-none tracking-tight flex items-center justify-center min-w-[28px] h-5',
                Number(item.actual_qty || 0) <= 0 ? 'bg-[#ef4444]' : 'bg-[#22c55e]'
              ]"
            >
              {{ Math.floor(item.actual_qty ?? 0) }}
            </div>

            <!-- Item Info -->
            <div class="min-w-0 pr-6">
              <span
                v-if="item.variant_of"
                class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200"
              >
                {{ item.variant_of }}
              </span>
              <h3 class="text-sm font-bold text-gray-900 truncate leading-snug mt-1" :title="item.item_name">
                {{ item.item_name || item.item_code }}
              </h3>
              <p class="text-xs text-gray-500 font-mono truncate">{{ item.item_code }}</p>
            </div>

            <!-- Price & Actions -->
            <div class="pt-1 border-t border-gray-100 flex items-center justify-between text-xs">
              <div v-if="item.selling_price != null" class="flex items-baseline gap-1">
                <span class="font-extrabold text-blue-600 text-sm">
                  ₹{{ Number(item.selling_price).toFixed(2) }}
                </span>
                <span class="text-gray-500 text-xs">/ {{ item.stock_uom || 'Nos' }}</span>
              </div>
              <span v-else class="text-xs text-amber-600 font-semibold bg-amber-50 px-1 py-0.5 rounded border border-amber-200">No price</span>

              <!-- Edit Price Button -->
              <button
                @click.stop="openPriceEditModal(item)"
                class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded transition"
                title="Edit / Set Selling Price"
              >
                <span class="lucide-pencil size-3.5" />
              </button>
            </div>
          </div>

          <div v-if="itemsTabFilteredList.length === 0" class="col-span-full py-12 text-center text-gray-400 text-sm">
            No items found. Create a brand or add an item above.
          </div>
        </div>
      </div>

      <!-- View 2: Invoices List View (Component-based Full Width) -->
      <InvoicesView
        v-show="currentTab === 'invoices'"
        :invoices="invoices"
        @print="printInvoice"
      />

      <!-- View 3: Purchase Entries (component) -->
      <PurchaseView
        v-show="currentTab === 'stock'"
        :entries="stockEntries"
        :items="items"
        @refresh="loadStockEntries"
      />
      </div>
    </div>

    <!-- Quick Add Customer Modal -->
    <div
      v-if="showAddCustomer"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <h2 class="text-sm font-bold text-gray-900">Add New Customer</h2>
        <div class="space-y-3">
          <div>
            <label class="text-[11px] font-semibold text-gray-600 block mb-1">Customer Name *</label>
            <input
              v-model="newCustomerName"
              type="text"
              placeholder="e.g. Ramesh Tailor"
              class="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="text-[11px] font-semibold text-gray-600 block mb-1">Mobile No (10 Digits)</label>
            <input
              v-model="newCustomerMobile"
              type="tel"
              maxlength="10"
              placeholder="e.g. 9876543210"
              @input="newCustomerMobile = newCustomerMobile.replace(/\D/g, '').slice(0, 10)"
              class="w-full border rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:ring-2"
              :class="newCustomerMobile && newCustomerMobile.length !== 10 ? 'border-red-400 focus:ring-red-400 bg-red-50/20' : 'border-gray-300 focus:ring-blue-500'"
            />
            <p v-if="newCustomerMobile && newCustomerMobile.length !== 10" class="text-[10px] text-red-500 mt-1">
              Mobile number must be exactly 10 digits ({{ newCustomerMobile.length }}/10)
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showAddCustomer = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            @click="addNewCustomer"
            :disabled="!newCustomerName.trim() || (newCustomerMobile && newCustomerMobile.length !== 10)"
            class="px-4 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Save
          </button>
        </div>
      </div>
    </div>

    <!-- Create Brand / Template Item Modal -->
    <div
      v-if="showCreateTemplateModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <div class="flex justify-between items-center border-b border-gray-100 pb-2">
          <h2 class="text-sm font-bold text-gray-900">Create Brand</h2>
          <button @click="showCreateTemplateModal = false" class="text-gray-400 hover:text-gray-600 text-sm">✕</button>
        </div>
        <p class="text-xs text-gray-500">Brands act as parent categories for all your items (e.g. Raymond, Kriplon, Siyaram).</p>
        <div class="space-y-3">
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Brand Name *</label>
            <input
              v-model="newTemplateName"
              type="text"
              placeholder="e.g. Raymond, Siyaram, Cotton-Fab"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Stock UOM</label>
            <select
              v-model="newTemplateUOM"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="Meter">Meter</option>
              <option value="Nos">Nos</option>
              <option value="Kg">Kg</option>
              <option value="Unit">Unit</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showCreateTemplateModal = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            @click="submitCreateTemplate"
            :disabled="isSubmittingTemplate"
            class="px-4 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm disabled:opacity-50"
          >
            <span v-if="isSubmittingTemplate">Creating...</span>
            <span v-else>Create Brand</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Create Item / Variant Modal -->
    <div
      v-if="showCreateVariantModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <div class="flex justify-between items-center border-b border-gray-100 pb-2">
          <h2 class="text-sm font-bold text-gray-900">Add Item</h2>
          <button @click="showCreateVariantModal = false" class="text-gray-400 hover:text-gray-600 text-sm">✕</button>
        </div>

        <div class="space-y-3">
          <!-- Choose Brand: Existing or Create New -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Select Brand *</label>
            <div class="flex gap-1.5">
              <select
                v-model="newVariantTemplate"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="" disabled>Select brand...</option>
                <option v-for="t in templates" :key="t.item_code" :value="t.item_code">
                  {{ t.item_name || t.item_code }}
                </option>
              </select>
              <button
                @click="showCreateVariantModal = false; showCreateTemplateModal = true"
                class="px-2.5 py-2 text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg whitespace-nowrap"
                title="Create a new brand"
              >
                + New Brand
              </button>
            </div>
          </div>

          <!-- Item Code/Identifier -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Item Code / Design No *</label>
            <input
              v-model="newVariantCode"
              type="text"
              placeholder="e.g. 004, Blue, 102"
              class="w-full border rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2"
              :class="isVariantAlreadyExists ? 'border-amber-400 bg-amber-50/40 text-amber-900 focus:ring-amber-400' : 'border-gray-300 focus:ring-blue-500'"
            />
            <div v-if="newVariantTemplate && newVariantCode" class="mt-1.5">
              <p class="text-[11px] text-gray-500">
                Full Item Code: <b class="font-mono text-gray-900">{{ fullVariantCode }}</b>
              </p>
              <div
                v-if="isVariantAlreadyExists"
                class="mt-1 flex items-center justify-between p-2 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-xs"
              >
                <div class="flex items-center gap-1.5">
                  <span class="lucide-alert-circle size-3.5 text-amber-600 flex-shrink-0" />
                  <span>Item already added!</span>
                </div>
                <button
                  type="button"
                  @click="showCreateVariantModal = false; openPriceEditModal(existingVariantItem)"
                  class="text-[11px] font-bold text-amber-900 hover:underline inline-flex items-center gap-0.5"
                >
                  <span>Edit Price (₹{{ existingVariantItem?.selling_price || 0 }})</span>
                  <span class="lucide-pencil size-3" />
                </button>
              </div>
            </div>
          </div>

          <!-- Selling Price -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Selling Price (₹)</label>
            <input
              v-model="newVariantPrice"
              type="number"
              step="0.01"
              placeholder="e.g. 450.00"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-3 border-t border-gray-100">
          <button
            type="button"
            @click="showCreateVariantModal = false"
            class="px-3 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="submitCreateVariant"
            :disabled="isSubmittingVariant || !newVariantTemplate || !newVariantCode.trim() || isVariantAlreadyExists"
            class="px-4 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1.5"
          >
            <span v-if="isSubmittingVariant" class="lucide-loader-2 size-3 animate-spin" />
            <span v-if="isSubmittingVariant">Saving...</span>
            <span v-else-if="isVariantAlreadyExists">Already Exists</span>
            <span v-else>Save Item</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Selling Price Modal -->
    <div
      v-if="showPriceEditModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-5 space-y-4">
        <div class="flex items-center justify-between border-b border-gray-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="lucide-pencil size-4 text-blue-600" />
            <h3 class="text-sm font-bold text-gray-900">Set Selling Price</h3>
          </div>
          <button
            @click="showPriceEditModal = false"
            class="text-gray-400 hover:text-gray-600 text-sm"
          >✕</button>
        </div>

        <div class="space-y-3">
          <div class="bg-gray-50 p-2.5 rounded-xl border border-gray-200 text-xs">
            <div class="font-bold text-gray-900">{{ editingItem?.item_name || editingItem?.item_code }}</div>
            <div class="text-gray-500 font-mono mt-0.5">{{ editingItem?.item_code }}</div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-700 mb-1">
              Rate / Price (₹ per {{ editingItem?.stock_uom || 'Unit' }})
            </label>
            <div class="relative">
              <span class="absolute left-3 top-2.5 text-gray-400 font-bold text-sm">₹</span>
              <input
                ref="priceInputRef"
                v-model.number="editingPriceValue"
                type="number"
                step="any"
                min="0"
                placeholder="0.00"
                @keydown.enter="submitUpdateItemPrice"
                class="w-full pl-7 pr-3 py-2 text-sm font-bold text-gray-900 bg-white border border-gray-300 rounded-[11px] focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showPriceEditModal = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-[11px] font-medium"
          >
            Cancel
          </button>
          <button
            @click="submitUpdateItemPrice"
            :disabled="isSubmittingPrice || editingPriceValue === '' || editingPriceValue == null"
            class="px-4 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-[11px] shadow-sm disabled:opacity-50"
          >
            <span v-if="isSubmittingPrice">Updating...</span>
            <span v-else>Update Price</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Success Dialog -->
    <div
      v-if="showSuccessDialog"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 text-center space-y-4">
        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-[11px] flex items-center justify-center mx-auto text-2xl font-bold shadow-xs">
          ✓
        </div>
        <div>
          <h2 class="text-base font-bold text-gray-900">Invoice Created Successfully</h2>
          <p class="text-xs text-gray-500 mt-0.5">Submitted directly without POS Profile</p>
        </div>

        <div class="bg-gray-50 rounded-xl p-3 border border-gray-200 text-left text-xs space-y-1.5">
          <div class="flex justify-between">
            <span class="text-gray-500">Invoice No:</span>
            <span class="font-extrabold text-gray-900">{{ lastInvoice?.name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Grand Total:</span>
            <span class="font-bold text-blue-600">₹{{ lastInvoice?.grand_total }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Status:</span>
            <span class="px-2 py-0.5 bg-green-100 text-green-700 font-bold rounded text-[10px]">{{ lastInvoice?.status }}</span>
          </div>
        </div>

        <div class="flex gap-2">
          <button
            v-if="lastInvoice?.name"
            @click="printInvoice(lastInvoice.name)"
            class="flex-1 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold rounded-xl transition flex items-center justify-center gap-1.5"
          >
            <span>🖨️</span>
            <span>Print Receipt</span>
          </button>
          <button
            @click="startNewSale"
            class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-md transition"
          >
            New Sale
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import InvoicesView from '../components/InvoicesView.vue';
import PurchaseView from '../components/PurchaseView.vue';

const customerSearchContainer = ref(null);

const currentTab = ref('pos');
const invoices = ref([]);
const stockEntries = ref([]);

// Items Tab State
const itemsTabSelectedTemplate = ref('');
const itemsSearchQuery = ref('');
const showCreateTemplateModal = ref(false);
const showCreateVariantModal = ref(false);
const isSubmittingTemplate = ref(false);
const isSubmittingVariant = ref(false);

const showPriceEditModal = ref(false);
const isSubmittingPrice = ref(false);
const editingItem = ref(null);
const editingPriceValue = ref('');
const priceInputRef = ref(null);

function openPriceEditModal(item) {
  editingItem.value = item;
  editingPriceValue.value = item.selling_price != null ? item.selling_price : '';
  showPriceEditModal.value = true;
  setTimeout(() => {
    priceInputRef.value?.focus();
    priceInputRef.value?.select();
  }, 100);
}

async function submitUpdateItemPrice() {
  if (!editingItem.value || editingPriceValue.value === '' || editingPriceValue.value == null) {
    alert('Please enter a valid price.');
    return;
  }
  const rate = parseFloat(editingPriceValue.value);
  if (isNaN(rate) || rate < 0) {
    alert('Please enter a valid positive number for price.');
    return;
  }
  isSubmittingPrice.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.update_item_price', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        item_code: editingItem.value.item_code,
        rate: rate,
      }),
    });
    const json = await res.json();
    if (json.message) {
      editingItem.value.selling_price = rate;
      const cartItem = cart.value.find((r) => r.item_code === editingItem.value.item_code);
      if (cartItem) {
        cartItem.rate = rate;
      }
      showPriceEditModal.value = false;
    } else {
      alert('Error updating price: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Failed to update price');
    console.error(err);
  } finally {
    isSubmittingPrice.value = false;
  }
}

const newTemplateName = ref('');
const newTemplateUOM = ref('Meter');
const newVariantTemplate = ref('');
const newVariantCode = ref('');
const newVariantPrice = ref('');

const fullVariantCode = computed(() => {
  if (!newVariantTemplate.value || !newVariantCode.value.trim()) return '';
  return `${newVariantTemplate.value}-${newVariantCode.value.trim()}`;
});

const isVariantAlreadyExists = computed(() => {
  if (!fullVariantCode.value) return false;
  return items.value.some(
    (item) => item.item_code.toLowerCase() === fullVariantCode.value.toLowerCase()
  );
});

const existingVariantItem = computed(() => {
  if (!fullVariantCode.value) return null;
  return items.value.find(
    (item) => item.item_code.toLowerCase() === fullVariantCode.value.toLowerCase()
  ) || null;
});

const searchQuery = ref('');
const customerSearchInput = ref('');
const isCustomerDropdownOpen = ref(false);
const selectedTemplate = ref('');
const loading = ref(false);
const isSubmitting = ref(false);
const showSuccessDialog = ref(false);
const showAddCustomer = ref(false);

const lastInvoice = ref(null);
const newCustomerName = ref('');
const newCustomerMobile = ref('');

const items = ref([]);
const templates = ref([]);
const customers = ref([]);
const paymentModes = ref(['Cash', 'UPI']);
const selectedCustomer = ref('');
const selectedPaymentMode = ref('Cash');
const splitCashAmount = ref(0);
const splitUpiAmount = ref(0);
const cart = ref([]);

function setPaymentMode(mode) {
  selectedPaymentMode.value = mode;
  if (mode === 'Split') {
    const half = Math.round((subtotal.value / 2) * 100) / 100;
    splitCashAmount.value = half;
    splitUpiAmount.value = Math.round((subtotal.value - half) * 100) / 100;
  }
}

function onSplitCashChange() {
  const cash = Math.max(0, Number(splitCashAmount.value) || 0);
  splitCashAmount.value = cash;
  splitUpiAmount.value = Math.max(0, Math.round((subtotal.value - cash) * 100) / 100);
}

function onSplitUpiChange() {
  const upi = Math.max(0, Number(splitUpiAmount.value) || 0);
  splitUpiAmount.value = upi;
  splitCashAmount.value = Math.max(0, Math.round((subtotal.value - upi) * 100) / 100);
}

const splitDifference = computed(() => {
  const allocated = Number(splitCashAmount.value || 0) + Number(splitUpiAmount.value || 0);
  return Math.round((subtotal.value - allocated) * 100) / 100;
});

const selectedCustomerDoc = computed(() => {
  return customers.value.find((c) => c.name === selectedCustomer.value) || null;
});

const searchedCustomers = computed(() => {
  if (!customerSearchInput.value) return customers.value;
  const q = customerSearchInput.value.toLowerCase();
  return customers.value.filter(
    (c) =>
      (c.customer_name && c.customer_name.toLowerCase().includes(q)) ||
      (c.name && c.name.toLowerCase().includes(q)) ||
      (c.mobile_no && c.mobile_no.includes(q))
  );
});

function toggleCustomerSearch() {
  selectedCustomer.value = '';
  customerSearchInput.value = '';
  isCustomerDropdownOpen.value = true;
}

function selectCustomer(cust) {
  selectedCustomer.value = cust.name;
  isCustomerDropdownOpen.value = false;
  customerSearchInput.value = '';
}

const filteredItems = computed(() => {
  return items.value.filter((i) => {
    const matchesSearch =
      !searchQuery.value ||
      (i.item_name && i.item_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (i.item_code && i.item_code.toLowerCase().includes(searchQuery.value.toLowerCase()));

    const matchesTemplate = !selectedTemplate.value || i.variant_of === selectedTemplate.value;

    return matchesSearch && matchesTemplate;
  });
});

const itemsTabFilteredList = computed(() => {
  return items.value.filter((i) => {
    const matchesSearch =
      !itemsSearchQuery.value ||
      (i.item_name && i.item_name.toLowerCase().includes(itemsSearchQuery.value.toLowerCase())) ||
      (i.item_code && i.item_code.toLowerCase().includes(itemsSearchQuery.value.toLowerCase()));

    const matchesTemplate = !itemsTabSelectedTemplate.value || i.variant_of === itemsTabSelectedTemplate.value;

    return matchesSearch && matchesTemplate;
  });
});

function openVariantModal(tmpl = '') {
  newVariantTemplate.value = tmpl || itemsTabSelectedTemplate.value || (templates.value[0]?.item_code || '');
  newVariantCode.value = '';
  newVariantPrice.value = '';
  showCreateVariantModal.value = true;
}

async function submitCreateTemplate() {
  if (!newTemplateName.value.trim()) {
    alert('Please enter template name');
    return;
  }
  isSubmittingTemplate.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.create_template_item', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        item_name: newTemplateName.value.trim(),
        stock_uom: newTemplateUOM.value || 'Meter',
      }),
    });
    const json = await res.json();
    if (json.message) {
      templates.value.unshift(json.message);
      itemsTabSelectedTemplate.value = json.message.item_code;
      showCreateTemplateModal.value = false;
      const createdTmpl = newTemplateName.value;
      newTemplateName.value = '';
      // Open variant creator immediately for ease
      openVariantModal(createdTmpl);
    } else {
      alert('Error creating template: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Failed to create template item');
  } finally {
    isSubmittingTemplate.value = false;
  }
}

async function submitCreateVariant() {
  if (!newVariantTemplate.value || !newVariantCode.value.trim()) {
    alert('Please choose template and variant suffix');
    return;
  }
  isSubmittingVariant.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.create_item_variant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        template_item: newVariantTemplate.value,
        variant_code: newVariantCode.value.trim(),
        selling_price: newVariantPrice.value ? Number(newVariantPrice.value) : null,
      }),
    });
    const json = await res.json();
    if (json.message) {
      items.value.unshift(json.message);
      showCreateVariantModal.value = false;
      newVariantCode.value = '';
      newVariantPrice.value = '';
    } else {
      alert('Error creating variant: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Failed to create item variant');
  } finally {
    isSubmittingVariant.value = false;
  }
}

const subtotal = computed(() => {
  return cart.value.reduce((acc, row) => acc + row.qty * row.rate, 0);
});

const totalQuantity = computed(() => {
  return cart.value.reduce((acc, row) => acc + row.qty, 0);
});

const selectedCustomerName = computed(() => {
  const c = customers.value.find((c) => c.name === selectedCustomer.value);
  return c ? c.customer_name || c.name : 'Customer';
});

function getItemCartQty(item_code) {
  const row = cart.value.find((r) => r.item_code === item_code);
  return row ? row.qty : 0;
}

function getStockStatus(qty) {
  const quantity = Math.floor(qty !== undefined && qty !== null ? qty : 0);
  if (quantity <= 0) {
    return {
      color: 'bg-red-500',
      textColor: 'text-white',
    };
  }
  if (quantity <= 10) {
    return {
      color: 'bg-amber-500',
      textColor: 'text-white',
    };
  }
  return {
    color: 'bg-emerald-600',
    textColor: 'text-white',
  };
}

function playAddSound() {
  try {
    const ctx = new AudioContext();
    const t = ctx.currentTime;

    function chime(freq, startAt, vol = 0.18) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0, startAt);
      gain.gain.linearRampToValueAtTime(vol, startAt + 0.008);
      gain.gain.exponentialRampToValueAtTime(0.001, startAt + 0.25);
      osc.start(startAt);
      osc.stop(startAt + 0.26);
    }

    // Two-note tap chime (C6 → E6)
    chime(1046.5, t);
    chime(1318.5, t + 0.1);

    // Soft physical tap body underneath
    const osc = ctx.createOscillator();
    const oscGain = ctx.createGain();
    osc.connect(oscGain);
    oscGain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(180, t);
    osc.frequency.exponentialRampToValueAtTime(90, t + 0.045);
    oscGain.gain.setValueAtTime(0.10, t);
    oscGain.gain.exponentialRampToValueAtTime(0.001, t + 0.05);
    osc.start(t);
    osc.stop(t + 0.05);
  } catch {}
}

function playPaymentSound() {
  try {
    const ctx = new AudioContext();
    const t = ctx.currentTime;

    const playNote = (freq, start, duration, volume = 0.12) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, start);
      gain.gain.setValueAtTime(0.001, start);
      gain.gain.exponentialRampToValueAtTime(volume, start + 0.008);
      gain.gain.exponentialRampToValueAtTime(0.001, start + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(start);
      osc.stop(start + duration);
    };

    playNote(880, t, 0.12, 0.10);
    playNote(1318.5, t + 0.09, 0.20, 0.12);
  } catch {}
}

function addToCart(item) {
  if (item.is_stock_item && Number(item.actual_qty || 0) <= 0) {
    alert(`Item "${item.item_name || item.item_code}" is out of stock (Available: 0).`);
    return;
  }
  if (item.selling_price == null) {
    alert(`Item ${item.item_code} does not have an active selling price.`);
    return;
  }
  const existing = cart.value.find((r) => r.item_code === item.item_code);
  if (existing) {
    if (item.is_stock_item && existing.qty >= Number(item.actual_qty || 0)) {
      alert(`Cannot add more than available stock (${item.actual_qty}).`);
      return;
    }
    existing.qty += 1;
  } else {
    cart.value.push({
      item_code: item.item_code,
      item_name: item.item_name || item.item_code,
      rate: Number(item.selling_price) || 0,
      qty: 1,
    });
  }
  playAddSound();
}

function updateCartRowQty(idx, rawVal) {
  const parsed = parseFloat(rawVal);
  if (isNaN(parsed) || parsed <= 0) {
    cart.value.splice(idx, 1);
    return;
  }
  const val = Math.round(parsed * 100) / 100;
  const row = cart.value[idx];
  const itemDoc = items.value.find((i) => i.item_code === row.item_code);
  if (itemDoc && itemDoc.is_stock_item && val > Number(itemDoc.actual_qty || 0)) {
    alert(`Cannot exceed available stock (${itemDoc.actual_qty}).`);
    row.qty = Number(itemDoc.actual_qty || 0);
    return;
  }
  row.qty = val;
}

function increaseQty(idx) {
  const row = cart.value[idx];
  const itemDoc = items.value.find((i) => i.item_code === row.item_code);
  const next = Math.round((row.qty + 1) * 100) / 100;
  if (itemDoc && itemDoc.is_stock_item && next > Number(itemDoc.actual_qty || 0)) {
    alert(`Cannot exceed available stock (${itemDoc.actual_qty}).`);
    return;
  }
  row.qty = next;
}

function decreaseQty(idx) {
  if (cart.value[idx].qty > 1) {
    cart.value[idx].qty = Math.round((cart.value[idx].qty - 1) * 100) / 100;
  } else {
    cart.value.splice(idx, 1);
  }
}

async function loadData() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_pos_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      items.value = json.message.items || [];
      templates.value = json.message.templates || [];
      customers.value = json.message.customers || [];
      paymentModes.value = json.message.modes_of_payment || ['Cash', 'UPI'];
      if (!selectedPaymentMode.value && paymentModes.value.length) {
        selectedPaymentMode.value = paymentModes.value[0];
      }
    }
  } catch (err) {
    console.error('Failed to load POS data', err);
  } finally {
    loading.value = false;
  }
}

async function addNewCustomer() {
  if (!newCustomerName.value.trim()) {
    alert('Customer name is required');
    return;
  }
  const cleanMobile = newCustomerMobile.value.trim();
  if (cleanMobile && cleanMobile.length !== 10) {
    alert('Mobile number must be exactly 10 digits');
    return;
  }
  try {
    const res = await fetch('/api/method/tailorms.api.create_customer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        customer_name: newCustomerName.value.trim(),
        mobile_no: cleanMobile,
      }),
    });
    const json = await res.json();
    if (json.message) {
      customers.value.unshift(json.message);
      selectedCustomer.value = json.message.name;
      newCustomerName.value = '';
      newCustomerMobile.value = '';
      showAddCustomer.value = false;
    }
  } catch (err) {
    alert('Failed to create customer');
  }
}

async function createInvoice() {
  if (!selectedCustomer.value) {
    alert('Please select a customer.');
    return;
  }
  if (cart.value.length === 0) return;

  isSubmitting.value = true;
  try {
    let paymentsPayload = [];
    if (selectedPaymentMode.value === 'Split') {
      const cash = Number(splitCashAmount.value) || 0;
      const upi = Number(splitUpiAmount.value) || 0;
      if (cash > 0) {
        paymentsPayload.push({
          mode_of_payment: 'Cash',
          amount: cash,
        });
      }
      if (upi > 0) {
        paymentsPayload.push({
          mode_of_payment: 'UPI',
          amount: upi,
        });
      }
      if (paymentsPayload.length === 0) {
        paymentsPayload.push({
          mode_of_payment: 'Cash',
          amount: subtotal.value,
        });
      }
    } else {
      paymentsPayload.push({
        mode_of_payment: selectedPaymentMode.value || 'Cash',
        amount: subtotal.value,
      });
    }

    const payload = {
      customer: selectedCustomer.value,
      items: cart.value.map((r) => ({
        item_code: r.item_code,
        qty: r.qty,
        rate: r.rate,
      })),
      payments: paymentsPayload,
      update_stock: 0,
    };

    const res = await fetch('/api/method/tailorms.api.create_sales_invoice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify(payload),
    });

    const json = await res.json();
    if (json.message && json.message.name) {
      playPaymentSound();
      lastInvoice.value = json.message;
      showSuccessDialog.value = true;
      cart.value = [];
    } else {
      alert('Error creating invoice: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Network error while creating invoice');
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
}

function formatDate(date) {
  if (!date) return '—';
  const [y, m, d] = String(date).split('-');
  return `${d}-${m}-${y}`;
}

function goToDesk() {
  window.location.href = '/desk';
}

function startNewSale() {
  showSuccessDialog.value = false;
  cart.value = [];
  selectedCustomer.value = '';
  customerSearchInput.value = '';
  searchQuery.value = '';
  selectedTemplate.value = '';
  selectedPaymentMode.value = paymentModes.value[0] || 'Cash';
  lastInvoice.value = null;
  loadData();
}

function printInvoice(invoiceName) {
  if (!invoiceName) return;
  const printUrl = `/printview?doctype=Sales+Invoice&name=${encodeURIComponent(invoiceName)}&format=${encodeURIComponent('Sales Invoice Bordered')}&no_letterhead=0`;
  window.open(printUrl, '_blank');
}

async function loadInvoices() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_invoices', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      invoices.value = json.message || [];
    }
  } catch (err) {
    console.error('Failed to load invoices', err);
  } finally {
    loading.value = false;
  }
}

async function loadStockEntries() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_stock_entries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      stockEntries.value = json.message || [];
    }
  } catch (err) {
    console.error('Failed to load stock entries', err);
  } finally {
    loading.value = false;
  }
}

function switchTab(tab) {
  currentTab.value = tab;
  if (tab === 'invoices') {
    loadInvoices();
  } else if (tab === 'stock') {
    loadStockEntries();
  }
}

function refreshCurrentTab() {
  if (currentTab.value === 'pos') {
    loadData();
  } else if (currentTab.value === 'invoices') {
    loadInvoices();
  } else if (currentTab.value === 'stock') {
    loadStockEntries();
  }
}

function handleGlobalClick(e) {
  if (
    isCustomerDropdownOpen.value &&
    customerSearchContainer.value &&
    !customerSearchContainer.value.contains(e.target)
  ) {
    isCustomerDropdownOpen.value = false;
  }
}

function handleGlobalKeydown(e) {
  if (e.key === 'Escape' && isCustomerDropdownOpen.value) {
    isCustomerDropdownOpen.value = false;
  }
}

onMounted(() => {
  loadData();
  document.addEventListener('click', handleGlobalClick);
  document.addEventListener('keydown', handleGlobalKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleGlobalClick);
  document.removeEventListener('keydown', handleGlobalKeydown);
});
</script>
