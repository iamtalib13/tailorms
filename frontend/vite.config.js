import path from "node:path";
import vue from "@vitejs/plugin-vue";
import frappeui from "frappe-ui/vite";
import { defineConfig } from "vite";

export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: true,
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				indexHtmlPath: "../tailorms/www/pos.html",
				outDir: "../tailorms/public/pos",
				emptyOutDir: true,
			},
		}),
		vue(),
	],
	build: {
		outDir: "../tailorms/public/pos",
		emptyOutDir: true,
		target: "es2015",
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
		},
	},
	server: {
		port: 8080,
		proxy: {
			"^/(app|api|assets|files)": {
				target: "http://127.0.0.1:8003",
				ws: true,
				changeOrigin: true,
			},
		},
	},
});
