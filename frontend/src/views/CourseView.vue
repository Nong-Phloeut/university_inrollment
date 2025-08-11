<template>
  <div>
    <custom-title>
      Course
      <template #right>
        <v-btn color="primary" @click="openDialog('add')">
          <v-icon left>mdi-plus</v-icon>
          Add course
        </v-btn>
      </template>
    </custom-title>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="medicationHeaders"
            :items="medications"
            items-per-page="10"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                color="secondary"
                size="small"
                class="mr-2"
                @click="openDialog('edit', item)"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon color="error" size="small" @click="deleteItem(item)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add/Edit Medication Dialog -->
    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h5 bg-primary">{{ formTitle }} Medication</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="editedItem.name"
              label="Medication Name"
              :rules="[(v) => !!v || 'Name is required']"
              required
            ></v-text-field>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.sku"
                  label="Stock Keeping Unit"
                  :rules="[(v) => !!v || 'SKU is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.category"
                  label="Category"
                  :rules="[(v) => !!v || 'Category is required']"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="editedItem.price"
                  label="Price ($)"
                  type="number"
                  :rules="[(v) => !!v || 'Price is required']"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="6"
                ><v-text-field
                  v-model="editedItem.stock"
                  label="Stock"
                  type="number"
                  :rules="[(v) => !!v || 'Stock is required']"
                  required
                ></v-text-field
              ></v-col>
            </v-row>

            <v-text-field
              v-model="editedItem.expiryDate"
              label="Expiry Date"
              type="date"
              :rules="[(v) => !!v || 'Expiry Date is required']"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="closeDialog">Cancel</v-btn>
          <v-btn color="primary" @click="saveItem">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useMedicationStore } from "../stores/medications";

const dialog = ref(false);
const editedItem = ref({
  id: null,
  name: "",
  sku: "",
  category: "",
  price: 0,
  stock: 0,
  expiryDate: "",
});
const editedIndex = ref(-1);

const store = useMedicationStore();
const medications = computed(() => store.medications);

const medicationHeaders = [
  { title: "Medication Name", key: "name" },
  { title: "SKU", key: "sku" },
  { title: "Category", key: "category" },
  { title: "Price ($)", key: "price" },
  { title: "Stock", key: "stock" },
  { title: "Expiry Date", key: "expiryDate" },
  { title: "Actions", key: "actions", sortable: false },
];

const formTitle = computed(() => (editedIndex.value === -1 ? "Add" : "Edit"));

const openDialog = (mode, item = null) => {
  if (mode === "add") {
    editedIndex.value = -1;
    editedItem.value = {
      id: null,
      name: "",
      sku: "",
      category: "",
      price: 0,
      stock: 0,
      expiryDate: "",
    };
  } else {
    editedIndex.value = medications.value.findIndex(m => m.id === item.id);
    editedItem.value = { ...item };
  }
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  editedItem.value = {
    id: null,
    name: "",
    sku: "",
    category: "",
    price: 0,
    stock: 0,
    expiryDate: "",
  };
  editedIndex.value = -1;
};

const saveItem = async () => {
  if (editedItem.value.id) {
    await store.updateMedication(editedItem.value.id, editedItem.value);
  } else {
    await store.createMedication(editedItem.value);
  }

  dialog.value = false;
};

const deleteItem = async (item) => {
  const confirmDelete = confirm("Are you sure you want to delete this medication?");
  if (confirmDelete) {
    await store.deleteMedication(item.id);
  }
};

onMounted(() => {
  store.fetchMedications();
});
</script>


<style scoped>
/* No scoped styles needed */
</style>
