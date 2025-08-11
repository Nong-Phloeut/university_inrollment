
<!-- views/PharmacistsView.vue -->
<template>
  <div>
    <custom-title>
      Instructors
      <template #right>
          <v-btn color="primary" @click="openDialog('add')">
          <v-icon left>mdi-plus</v-icon>
          Add Instructors
        </v-btn>
      </template>
    </custom-title>
    
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="pharmacistHeaders"
            :items="pharmacists"
            items-per-page="10"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn icon color="secondary" size="small" class="mr-2" @click="openDialog('edit', item)">
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

    <!-- Add/Edit Pharmacist Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5 bg-primary">{{ formTitle }} Pharmacist</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="editedItem.name"
              label="Name"
              :rules="[v => !!v || 'Name is required']"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.email"
              label="Email"
              :rules="[v => !!v || 'Email is required']"
              required
            ></v-text-field>
            <v-select
              v-model="editedItem.status"
              :items="['Active', 'Inactive']"
              label="Status"
              :rules="[v => !!v || 'Status is required']"
              required
            ></v-select>
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
import { ref, computed } from 'vue';

const dialog = ref(false);
const valid = ref(true);
const editedItem = ref({
  id: null,
  name: '',
  email: '',
  status: 'Active',
});
const editedIndex = ref(-1);

const pharmacistHeaders = [
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Status', key: 'status' },
  { title: 'Actions', key: 'actions', sortable: false },
];

const pharmacists = ref([
  { id: 1, name: 'John Doe', email: 'john.doe@pharmacy.com', status: 'Active' },
  { id: 2, name: 'Jane Smith', email: 'jane.smith@pharmacy.com', status: 'Active' },
  { id: 3, name: 'Peter Jones', email: 'peter.jones@pharmacy.com', status: 'Inactive' },
]);

const formTitle = computed(() => editedIndex.value === -1 ? 'Add' : 'Edit');

const openDialog = (mode, item = null) => {
  if (mode === 'add') {
    editedIndex.value = -1;
    editedItem.value = { id: null, name: '', email: '', status: 'Active' };
  } else {
    editedIndex.value = pharmacists.value.indexOf(item);
    editedItem.value = { ...item };
  }
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  editedItem.value = { id: null, name: '', email: '', status: 'Active' };
  editedIndex.value = -1;
};

const saveItem = () => {
  if (editedIndex.value > -1) {
    Object.assign(pharmacists.value[editedIndex.value], editedItem.value);
  } else {
    editedItem.value.id = pharmacists.value.length + 1;
    pharmacists.value.push(editedItem.value);
  }
  closeDialog();
};

const deleteItem = (item) => {
  const index = pharmacists.value.indexOf(item);
  if (confirm('Are you sure you want to delete this pharmacist?')) {
    pharmacists.value.splice(index, 1);
  }
};
</script>

<style scoped>
/* No scoped styles needed */
</style>