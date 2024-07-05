import type { ConfigFile } from "@rtk-query/codegen-openapi"

const config: ConfigFile = {
  schemaFile: "http://localhost:8000/openapi.json",
  apiFile: "./src/store/baseApi.ts",
  apiImport: "baseApi",
  outputFile: "./src/store/coreApi2.ts",
  exportName: "coreApi",
  hooks: true,
}

export default config
