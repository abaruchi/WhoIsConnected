CREATE TABLE "device" (
  "mac_addr" TEXT NOT NULL CONSTRAINT "pk_device" PRIMARY KEY,
  "name" TEXT NOT NULL,
  "eth_vendor" TEXT NOT NULL,
  "cur_status" TEXT NOT NULL
);

CREATE TABLE "connecttime" (
  "id" UUID NOT NULL CONSTRAINT "pk_connecttime" PRIMARY KEY,
  "lease_time" TEXT NOT NULL,
  "time" DATETIME NOT NULL,
  "transition" INTEGER,
  "device" TEXT NOT NULL REFERENCES "device" ("mac_addr")
);

CREATE INDEX "idx_connecttime__device" ON "connecttime" ("device")