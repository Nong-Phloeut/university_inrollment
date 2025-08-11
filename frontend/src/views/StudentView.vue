<template>
  <div>
    <custom-title>
      Students
      <template #right>
         <v-btn color="primary" @click="openDialog('add')">
          <v-icon left>mdi-plus</v-icon>
          Add Students
        </v-btn>
      </template>
    </custom-title>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-data-table
            :headers="adminHeaders"
            :items="userList"
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

    <!-- Add/Edit Admin Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5 bg-primary">{{ formTitle }} Admin</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="editedItem.name"
              label="Name"
              :rules="[(v) => !!v || 'Name is required']"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.email"
              label="Email"
              :rules="[(v) => !!v || 'Email is required']"
              required
            ></v-text-field>
            <v-select
              v-model="editedItem.role"
              :items="['Super Admin', 'Admin']"
              label="Role"
              :rules="[(v) => !!v || 'Role is required']"
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
import { ref, computed, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

const dialog = ref(false);
const valid = ref(true);
const editedItem = ref({
  id: null,
  name: "",
  email: "",
  role: "Admin",
});

const editedIndex = ref(-1);

const store = useUserStore();
const userList = computed(() => store.users);

const adminHeaders = [
  { title: "Name", key: "name" },
  { title: "Email", key: "email" },
  { title: "Role", key: "role" },
  { title: "Actions", key: "actions", sortable: false },
];

const formTitle = computed(() =>
  editedIndex.value === -1 ? "Add" : "Edit"
);

const openDialog = (mode, item = null) => {
  if (mode === "add") {
    editedIndex.value = -1;
    editedItem.value = { id: null, name: "", email: "", role: "Admin" };
  } else {
    editedIndex.value = userList.value.findIndex((u) => u.id === item.id);
    editedItem.value = { ...item };
  }
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  editedItem.value = { id: null, name: "", email: "", role: "Admin" };
  editedIndex.value = -1;
};

const saveItem = async () => {
  if (editedItem.value.id) {
    // Update user
    await store.updateUser(editedItem.value.id, editedItem.value);
  } else {
    // Create new user
    await store.createUser(editedItem.value);
  }

  // Refresh user list
  await store.fetchUsers();
  closeDialog();
};

const deleteItem = async (item) => {
  const confirmDelete = confirm("Are you sure you want to delete this admin?");
  if (!confirmDelete) return;

  await store.deleteUser(item.id);
  await store.fetchUsers();
};

onMounted(() => {
  store.fetchUsers();
});
</script>
