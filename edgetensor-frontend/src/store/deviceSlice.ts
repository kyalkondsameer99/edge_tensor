import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export interface Device {
  device_id: string;
  name?: string;
  license_plate?: string;
  imei?: string;
  lat?: number;
  lng?: number;
}

interface DeviceState {
  devices: Device[];
  selectedDevice: string | null;
  loading: boolean;
}

const initialState: DeviceState = {
  devices: [],
  selectedDevice: null,
  loading: false,
};

export const fetchDevices = createAsyncThunk<Device[]>(
  'devices/fetchDevices',
  async () => {
    const res = await fetch('/api/v2.0/devices/matrack');
    return await res.json();
  }
);

const deviceSlice = createSlice({
  name: 'devices',
  initialState,
  reducers: {
    setSelectedDevice(state, action: PayloadAction<string | null>) {
      state.selectedDevice = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDevices.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchDevices.fulfilled, (state, action) => {
        state.devices = action.payload;
        state.loading = false;
      })
      .addCase(fetchDevices.rejected, (state) => {
        state.loading = false;
      });
  },
});

export const { setSelectedDevice } = deviceSlice.actions;
export default deviceSlice.reducer; 