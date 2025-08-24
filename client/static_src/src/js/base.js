import Alpine from 'alpinejs'
import { Grid } from "gridjs";
import "gridjs/dist/theme/mermaid.css";
import intersect from '@alpinejs/intersect'
 
window.Alpine = Alpine
 
Alpine.plugin(intersect)
Alpine.start()