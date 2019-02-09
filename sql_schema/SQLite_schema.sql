CREATE TABLE "Device" (
  "mac_addr" TEXT NOT NULL PRIMARY KEY,
  "name" TEXT NOT NULL,
  "eth_vendor" TEXT NOT NULL,
  "cur_status" TEXT NOT NULL
);

CREATE TABLE "ConnectTime" (
  "id" UUID NOT NULL PRIMARY KEY,
  "lease_time" TEXT NOT NULL,
  "time" TEXT NOT NULL,
  "transition" TEXT NOT NULL,
  "device" TEXT NOT NULL REFERENCES "Device" ("mac_addr") ON DELETE CASCADE
);

CREATE INDEX "idx_connecttime__device" ON "ConnectTime" ("device");

CREATE TABLE "IPLease" (
  "id" UUID NOT NULL PRIMARY KEY,
  "IPv4Addr" TEXT,
  "IPv6Addr" TEXT,
  "Current" BOOLEAN,
  "device" TEXT NOT NULL REFERENCES "Device" ("mac_addr") ON DELETE CASCADE
);

CREATE INDEX "idx_iplease__device" ON "IPLease" ("device")
