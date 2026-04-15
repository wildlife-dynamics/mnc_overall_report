"""
Generate the MNC Overall Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_overall_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_overall_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Overall Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Overall Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Weather, logistics, livestock, wildlife, and patrol reporting for "
      "Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_overall_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_overall_report</b> workflow is a comprehensive, multi-pipeline "
      "report for Mara North Conservancy. It pulls data from two sources "
      "— EarthRanger weather station observations and EarthRanger event records — "
      "and routes them through five independent reporting sections:"),
    bullet("<b>Section 1 — Weather:</b> Observations from the GMMF weather station "
           "subject group; produces a daily summary CSV and 7 line charts."),
    bullet("<b>Section 2 — Logistics:</b> Balloon landings, airstrip operations, "
           "airstrip maintenance, and airline complaint events; produces 3 CSVs."),
    bullet("<b>Section 3 — Livestock:</b> Mobile boma movements, cattle counts, "
           "livestock predation, and illegal grazing events; produces 4 CSVs and "
           "3 maps."),
    bullet("<b>Section 4 — Wildlife:</b> Nine wildlife sighting types and five "
           "incident types; produces multiple CSVs, maps, and bar charts."),
    bullet("<b>Section 5 — Patrol:</b> Foot, vehicle, and motorbike patrol "
           "trajectories derived from patrol_info events; produces patrol effort "
           "CSVs, trajectory files, patrol coverage map, and occupancy statistics."),
    sp(4),
    p("All five sections share a single <b>events_temporal</b> DataFrame from "
      "one <b>get_events</b> call. Weather data uses a separate "
      "<b>get_subjectgroup_observations</b> call. The workflow concludes by "
      "generating a populated Word report from a Dropbox template."),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Section", "Output type", "Key files"],
            ["Weather",    "CSV + HTML charts",
             "weather_summary_table.csv, 7 × *_readings_over_time.html/.png"],
            ["Logistics",  "CSV",
             "balloon_landing_summary_table.csv, airstrip_operations_summary_table.csv, "
             "airstrip_maintenance_summary_table.csv"],
            ["Livestock",  "CSV + Map",
             "mobile_boma_movement_summary_table.csv, total_cattle_count_summary_table.csv, "
             "total_livestock_predation_summary_table.csv, livestock_predation_summary_table.csv, "
             "boma_movement_map, livestock_predation_events, illegal_grazing_map"],
            ["Wildlife",   "CSV + Map + Chart",
             "total_*_events_recorded.csv (7 species), individual summaries (lion, leopard, "
             "cheetah), wildlife incident CSVs, sighting maps, herd bar charts"],
            ["Patrol",     "CSV + GeoJSON + Map",
             "foot/vehicle/motorbike/overall_patrol_efforts.csv, trajectories.geojson, "
             "patrol_coverage.csv, patrol_coverage_map.html"],
            ["Report",     "Word document",
             "overall_report.docx"],
        ],
        [2.5*cm, 2.5*cm, W - 5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.45.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.19.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "0.0.14.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.9.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch all event records and subject group observations; "
             "also used by process_events_details calls to resolve display titles."],
            ["mnc_conservancy.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundaries split by grazing zone. "
             "Used as base polygon layers on all livestock, wildlife, and patrol maps."],
            ["mnc_across_the_river_parcels.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels. "
             "Used as an additional polygon layer on selected maps."],
            ["mara_north_event_template.docx", "fetch_and_persist_file (Dropbox)",
             "Word report template. Populated by generate_mnc_report at the "
             "end of the workflow to produce overall_report.docx."],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("All Dropbox files are downloaded with overwrite_existing: false and "
         "retries: 3. If a file already exists in ECOSCOPE_WORKFLOWS_RESULTS "
         "from a prior run the download is skipped."),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All records are processed as a single undivided dataset — no fan-out or "
      "per-group branching is applied. The grouper is passed through to the "
      "temporal index and the dashboard only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before the reporting sections run, the workflow downloads and prepares "
      "all shared geospatial base layers. These layers are reused across all "
      "livestock, wildlife, and patrol maps."),
    sp(6),
    h2("3.1  Conservancy boundaries"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> from Dropbox "
             "(overwrite_existing: false, retries: 3)."],
            ["2", "load_df",
             "Load the gpkg into a GeoDataFrame (layer: null, deserialize_json: false)."],
            ["3", "split_gdf_by_column",
             "Split the GeoDataFrame into a dict keyed by the <b>grazing_zone</b> "
             "column (Conservancy, Conservancy Herd Zone, Grazing Zone 1–4)."],
            ["4", "annotate_gdf_dict_with_geom_type",
             "Add geometry-type attributes to each GDF in the dict "
             "(ecoscope_workflows_ext_ste task)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Styled zone layers"),
    p("Two separate DeckGL layer sets are built from the annotated dict:"),
    make_table(
        [
            ["Layer set", "Task", "Zones included", "Used on"],
            ["create_mnc_styled_layers",
             "create_deckgl_layers_from_gdf_dict",
             "All six zones: Conservancy (grey outline), Conservancy Herd Zone "
             "(green), Grazing Zones 1–4 (dark olive, teal, dark green, sage)",
             "Boma movement map, illegal grazing map, patrol maps"],
            ["create_conservancy_boundaries",
             "create_deckgl_layers_from_gdf_dict",
             "Conservancy boundary only (grey outline, no fill). "
             "Legend: single 'Boundaries' entry.",
             "Livestock predation map, all wildlife sighting maps"],
        ],
        [3.5*cm, 3.5*cm, 3.5*cm, W - 10.5*cm],
    ),
    sp(6),
    h2("3.3  Conservancy GDFs and text labels"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "create_gdf_from_dict",
             "Extract the <b>Conservancy</b> key from the split dict → "
             "<b>conservancy_gdf</b>. Used for text label placement."],
            ["2", "filter_df",
             "Filter the full loaded GDF to rows where "
             "grazing_zone != 'Conservancy' → <b>overall_grazing_zones</b>. "
             "Used to compute the global map zoom and view state."],
            ["3", "create_custom_text_layer",
             "Render conservancy name labels using the <b>name</b> field from "
             "conservancy_gdf. Key params: get_size: 1500 m, size_min_pixels: 70, "
             "size_max_pixels: 100, size_scale: 2.25, font_family: Calibri, "
             "font_weight: 700, billboard: true, use_centroid: true."],
            ["4", "view_state_deck_gdf",
             "Compute the global map centre and zoom from overall_grazing_zones "
             "(pitch: 0, bearing: 0). Stored as <b>global_zoom_value</b> and "
             "shared by all maps except the livestock predation map."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.4  Parcels layer"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_across_the_river_parcels.gpkg</b> from Dropbox."],
            ["2", "load_df",
             "Load the parcels gpkg into a GeoDataFrame."],
            ["3", "get_gdf_geom_type",
             "Detect and attach the geometry type "
             "(ecoscope_workflows_ext_ste task)."],
            ["4", "create_deckgl_layer_from_gdf",
             "Render as a filled polygon layer: dark khaki fill (#bdb76b), "
             "opacity 0.15, stroked. Legend: 'Parcels'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. SHARED EVENT INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Shared Event Ingestion Pipeline"),
    hr(),
    p("All five reporting sections — logistics, livestock, wildlife, and patrol — "
      "share a single event retrieval call. Weather data uses a separate "
      "subject-group observation fetch."),
    sp(6),
    h2("4.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                      "get_events"],
            ["event_types",               "[] (fetch all event types)"],
            ["Columns retained",          "id, time, event_type, event_category, "
                                          "reported_by, serial_number, geometry, "
                                          "created_at, event_details, patrols"],
            ["include_details",           "true"],
            ["raise_on_empty",            "true"],
            ["include_null_geometry",     "false"],
            ["include_updates",           "false"],
            ["include_related_events",    "false"],
            ["include_display_values",    "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("4.2  Date extraction and temporal indexing"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new column named <b>date</b>."],
            ["2", "add_temporal_index",
             "Add temporal index using <b>time_col: date</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed. "
             "Produces the shared <b>events_temporal</b> DataFrame."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.3  Common event detail normalisation pattern"),
    p("Every event branch applies the same three-step normalisation after filtering "
      "events_temporal by event_type:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true, ordered: true). Requires the ER client."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["3", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened columns "
             "(duplicate_strategy: keep_original)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Because map_to_titles is true, flattened column names are "
         "human-readable display titles from EarthRanger (e.g. 'Balloon Company', "
         "'Livestock Species'). All downstream map_columns steps reference "
         "these titles directly."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. SECTION 1 — WEATHER PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Section 1 — Weather Pipeline"),
    hr(),
    p("The weather pipeline runs independently from the shared event pipeline. "
      "It fetches sensor observations from the <b>ER2ER - From GMMF</b> subject "
      "group and extracts seven meteorological fields sequentially from the "
      "<b>extra__observation_details</b> JSON column."),
    sp(6),
    h2("5.1  Observation retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                "get_subjectgroup_observations"],
            ["subject_group_name",  "ER2ER - From GMMF"],
            ["filter",              "clean"],
            ["raise_on_empty",      "false"],
            ["include_details",     "false"],
            ["include_subjectsource_details", "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("5.2  Field extraction chain"),
    p("Seven sequential <b>extract_value_from_json_column</b> tasks are chained, "
      "each reading from the previous task's output. All use "
      "<b>output_type: float</b> and extract from "
      "<b>extra__observation_details</b>:"),
    make_table(
        [
            ["Task id", "field_name_options", "output_column_name"],
            ["extract_precipitation",    "precipitation",          "precipitation"],
            ["extract_temperature",      "surface_air_temperature","temperature"],
            ["extract_wind_speed",       "wind_speed",             "wind_speed"],
            ["extract_wind_gusts",       "wind_gusts",             "wind_gusts"],
            ["extract_soil_temperature", "soil_temperature",       "soil_temperature"],
            ["extract_relative_humidity","relative_humidity",      "relative_humidity"],
            ["extract_pressure",         "atmospheric_pressure",   "atmospheric_pressure"],
        ],
        [4*cm, 5*cm, W - 9*cm],
    ),
    sp(6),
    h2("5.3  Date extraction, renaming, and temporal index"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>fixtime</b> column as <b>output_type: date</b> "
             "→ new column <b>date</b>."],
            ["2", "map_columns",
             "Rename <b>extra__subject__name</b> → <b>weather_station</b> "
             "(raise_if_not_found: true)."],
            ["3", "add_temporal_index",
             "Add temporal index using <b>time_col: fixtime</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.4  Daily weather summary"),
    p("Task: <b>summarize_df</b>. Groups by <b>weather_station</b> and <b>date</b>. "
      "Aggregations:"),
    make_table(
        [
            ["Column", "Aggregator", "Description"],
            ["precipitation",       "sum",  "Total daily rainfall (mm)"],
            ["temperature",         "mean", "Daily average temperature (°C)"],
            ["wind_speed",          "mean", "Daily average wind speed"],
            ["wind_gusts",          "max",  "Daily maximum wind gust"],
            ["soil_temperature",    "mean", "Daily average soil temperature (°C)"],
            ["relative_humidity",   "mean", "Daily average relative humidity (%)"],
            ["atmospheric_pressure","mean", "Daily average atmospheric pressure"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    p("Output saved as <b>weather_summary_table.csv</b>."),
    sp(6),
    h2("5.5  Line charts"),
    p("Seven <b>draw_line_chart</b> tasks read from the daily_weather DataFrame "
      "(x_column: date, category_column: weather_station, shape: linear). "
      "Charts are saved as HTML then batch-converted to PNG via a single "
      "<b>html_to_png</b> call (width: 1280, height: 720, device_scale_factor: 2.0, "
      "wait_for_timeout: 15 ms, max_concurrent_pages: 5):"),
    make_table(
        [
            ["HTML filename", "y_column", "y-axis label"],
            ["precipitation_readings_over_time.html",   "precipitation",
             "Precipitation (mm)"],
            ["temperature_readings_over_time.html",     "temperature",
             "Average Temperature (°C)"],
            ["wind_speed_readings_over_time.html",      "wind_speed",
             "Average wind speed"],
            ["wind_gusts_readings_over_time.html",      "wind_gusts",
             "Max wind gusts"],
            ["soil_temperature_readings_over_time.html","soil_temperature",
             "Average Temperature (°C)"],
            ["relative_humidity_readings_over_time.html","relative_humidity",
             "Average humidity"],
            ["atmospheric_pressure_readings_over_time.html","atmospheric_pressure",
             "Average pressure"],
        ],
        [6*cm, 3.5*cm, W - 9.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. SECTION 2 — LOGISTICS REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Section 2 — Logistics Report"),
    hr(),
    p("Four event types are filtered from <b>events_temporal</b> and "
      "normalised using the common three-step pattern (Section 4.3)."),
    sp(6),
    h2("6.1  Branch 1 — Balloon Landings"),
    p("Filter: event_type == <b>balloon_landing</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain date, Balloon Company, Where are clients staying?, # of passengers. "
             "Rename: Balloon Company → balloon_company, "
             "Where are clients staying? → where_are_clients_staying, "
             "# of passengers → no_of_passengers. (raise_if_not_found: false)"],
            ["5", "remove_brackets_from_column",
             "Strip bracket characters from balloon_company and "
             "where_are_clients_staying."],
            ["6", "persist_df",
             "Save as <b>balloon_landing_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.2  Branch 2 — Airstrip Operations"),
    p("Filter: event_type == <b>airstrip_operations</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Rename: Airline → airline, Arrival or departure → arrival_departure, "
             "Attendant → attendant, Camp/Lodge → camp_lodge, "
             "Number of clients → no_of_clients. "
             "(retain_columns: [], raise_if_not_found: false)"],
            ["5", "remove_brackets_from_column",
             "Strip bracket characters from airline, arrival_departure, "
             "attendant, camp_lodge."],
            ["6", "replace_missing_with_label",
             "Fill null camp_lodge values with <b>'other'</b>."],
            ["7", "convert_to_int",
             "Cast no_of_clients to integer (errors: coerce, fill_value: 0)."],
            ["8", "capitalize_text",
             "Capitalize text in the camp_lodge column."],
            ["9", "summarize_df",
             "Group by camp_lodge and arrival_departure; sum no_of_clients. "
             "reset_index: true."],
            ["10", "pivot_df",
             "Pivot: index_col: camp_lodge, columns_col: arrival_departure, "
             "values_col: no_of_clients."],
            ["11", "convert_to_int",
             "Cast arrival and departure columns to integer (fill_value: 0)."],
            ["12", "persist_df",
             "Save as <b>airstrip_operations_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.3  Branch 3 — Airstrip Maintenance"),
    p("Filter: event_type == <b>airstrip_maintenance</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["4", "map_columns",
             "Retain date, Maintenance type. "
             "Rename: Maintenance type → maintenance_type. (raise_if_not_found: false)"],
            ["5", "persist_df",
             "Save as <b>airstrip_maintenance_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.4  Branch 4 — Airline Complaints"),
    p("Filter: event_type == <b>airline_complaint</b>. "
      "This branch ends at the normalisation step "
      "(process_events_details → normalize_json_column → drop_column_prefix). "
      "No column selection, renaming, or persistence is defined."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. SECTION 3 — LIVESTOCK REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Section 3 — Livestock Report"),
    hr(),
    p("Four livestock event types are filtered from <b>events_temporal</b> "
      "and each normalised using the common pattern (Section 4.3)."),
    sp(6),
    h2("7.1  Branch 1 — Mobile Boma Movements"),
    p("Filter: event_type == <b>mobile_boma_rep</b>"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_mobile_prefix."],
            ["4", "map_columns",
             "Retain id, date, event_type, geometry, Date of Relocation, "
             "Electric Boma Status, Mobile Boma Zone, Nature of the Site, "
             "Reason for relocation. (raise_if_not_found: false)"],
            ["5", "summarize_df",
             "Group by date; count nunique(id) → boma_events (decimal_places: 0). "
             "reset_index: true."],
            ["6", "add_totals_row",
             "Append a Total row (label_col: date, label: Total)."],
            ["7", "persist_df",
             "Save as <b>mobile_boma_movement_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Map pipeline: exclude_geom_outliers (z=3) → drop_null_geometry → "
      "apply_color_map (event_type, tab20 → event_type_colors) → "
      "create_scatterplot_layer (legend: 'Boma Movements') → "
      "combine with MNC styled layers + parcels + text labels → draw_map → "
      "persist as <b>boma_movement_map.html</b> → html_to_png (scale: 2.0, wait: 40 s)."),
    sp(6),
    h2("7.2  Branch 2 — Cattle Counts"),
    p("Filter: event_type == <b>cattle_count</b>. No map produced."),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_cattle_prefix."],
            ["4", "map_columns",
             "Retain date, # cattle in Zone 1 mobile boma, # cattle in Zone 2/3 mobile boma, "
             "# cattle in Zone 4, total_cattle_counted_from_all_zones. "
             "Rename to zone_1, zone_2_3, zone_4, total_count."],
            ["5", "persist_df",
             "Save as <b>total_cattle_count_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("7.3  Branch 3 — Livestock Predation"),
    p("Filter: event_type == <b>livestock_predation_rep</b>. "
      "Produces two independent CSVs and one map."),
    h3("7.3a  total_livestock_predation_summary_table.csv"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_predation_prefix."],
            ["4", "map_columns",
             "Retain id, date, event_type, geometry, Livestock Species, "
             "Suspected Predator, Total livestock affected."],
            ["5", "summarize_df",
             "Group by date; count nunique(id) → livestock_predation_events. "
             "reset_index: true."],
            ["6", "add_totals_row", "Append a Total row."],
            ["7", "persist_df",
             "Save as <b>total_livestock_predation_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(4),
    h3("7.3b  livestock_predation_summary_table.csv"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "map_columns",
             "Retain date, Livestock Species, Suspected Predator, "
             "Total livestock affected. Rename to livestock_species, "
             "suspected_predator, total_livestock_affected."],
            ["2", "replace_missing_with_label",
             "Replace nulls in suspected_predator and livestock_species → 'Unknown'."],
            ["3", "map_column_values",
             "Map 'Other (specify in comments)' → 'Unknown' in suspected_predator."],
            ["4", "convert_to_int",
             "Cast total_livestock_affected to int (errors: coerce, fill_value: 0)."],
            ["5", "persist_df",
             "Save as <b>livestock_predation_summary_table.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(4),
    p("Map pipeline: exclude_geom_outliers (z=3) → drop_null_geometry → "
      "apply_color_map (Livestock Species, tab20 → colors) → "
      "create_scatterplot_layer (legend: 'Livestock Species') → "
      "combine with conservancy boundaries + parcels + text labels → "
      "draw_map (fixed view state: lon 35.2093, lat -1.2578, zoom 9.75) → "
      "persist as <b>livestock_predation_events.html</b> → html_to_png."),
    sp(6),
    h2("7.4  Branch 4 — Illegal Grazing"),
    p("Filter: event_type == <b>illegal_grazing_rep</b>. No CSV summary produced."),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1–3", "normalise",
             "process_events_details → normalize_json_column → drop_illegal_prefix."],
            ["4", "map_columns",
             "Retain date, event_type, geometry, Herd Zone, Landowner name, "
             "action taken. (raise_if_not_found: false)"],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Map pipeline: exclude_geom_outliers (z=3) → drop_null_geometry → "
      "apply_color_map (event_type, tab20 → event_type_colors) → "
      "create_scatterplot_layer (legend: 'Illegal grazing') → "
      "combine with MNC styled layers + text labels (no parcels) → "
      "draw_map (global_zoom_value) → persist as <b>illegal_grazing_map.html</b> → "
      "html_to_png."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. SECTION 4 — WILDLIFE REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Section 4 — Wildlife Report"),
    hr(),
    p("Nine wildlife species sighting types and five wildlife incident types "
      "are filtered from <b>events_temporal</b>. All sighting branches follow "
      "the common normalisation pattern (Section 4.3) and produce a daily "
      "event count CSV, a sighting map, and (for elephant and buffalo) "
      "an additional herd-size map and bar chart. Lion, leopard, and cheetah "
      "also produce an individual/pride summary CSV."),
    sp(6),
    h2("8.1  Common wildlife sighting pattern"),
    p("Each sighting branch applies:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal by event_type (op: equal, reset_index: true)."],
            ["2–4", "normalise",
             "process_events_details → normalize_json_column → drop_column_prefix."],
            ["5", "map_columns",
             "Drop audit columns (index, time, event_category, reported_by, "
             "serial_number). Rename species-specific fields to snake_case."],
            ["6", "replace_missing_with_label",
             "Fill null herd/group composition field with 'Unspecified'."],
            ["7", "convert_to_int",
             "Cast numeric count fields to integer (errors: coerce, fill_value: 0)."],
            ["8", "map_column_values",
             "Standardise composition values to Title Case "
             "(e.g. bachelor → Bachelor, mixed → Mixed)."],
            ["9", "summarize_df",
             "Group by date; count nunique(id) → no_of_events. "
             "reset_index: true."],
            ["10", "add_totals_row",
             "Append a Total row."],
            ["11", "persist_df",
             "Save daily count CSV (see table below)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("8.2  Sighting branches and daily count CSV outputs"),
    make_table(
        [
            ["Branch", "event_type value", "CSV output", "Map filename"],
            ["Elephant", "elephant_sighting_rep",
             "total_elephants_events_recorded.csv",
             "elephant_sightings_events.html/.png"],
            ["Buffalo",  "buffalo_sighting_rep",
             "total_buffalo_events_recorded.csv",
             "buffalo_sightings_events.html/.png"],
            ["Rhino",    "rhino_sighting_rep",
             "total_rhino_events_recorded.csv",
             "rhino_sightings_events.html/.png"],
            ["Lion",     "lion_sighting_rep",
             "total_lion_events_recorded.csv",
             "lion_sightings_events.html/.png"],
            ["Leopard",  "leopardsightingrep",
             "total_leopard_events_recorded.csv",
             "leopard_sightings_events.html/.png"],
            ["Cheetah",  "cheetah_sighting_rep",
             "total_cheetah_events_recorded.csv",
             "cheetah_sightings_events.html/.png"],
            ["Giraffe",  "giraffe_sighting",
             "— (no CSV)",
             "giraffe_sightings_events.html/.png"],
            ["Hartebeest","hartebeest_sighting",
             "— (no CSV)",
             "hartebeest_sightings_events.html/.png"],
        ],
        [2*cm, 3.5*cm, 4.5*cm, W - 10*cm],
    ),
    note("Giraffe and hartebeest branches produce only a sighting map — no daily "
         "count CSV is persisted for these two species."),
    sp(6),
    h2("8.3  Individual / pride summary CSVs"),
    p("Lion, leopard, and cheetah produce an additional summary grouped by a "
      "categorical identifier:"),
    make_table(
        [
            ["Branch", "Group-by column", "CSV output"],
            ["Lion",    "pride",      "individual_lions_summary.csv — sighting count per pride"],
            ["Leopard", "(individual identifier)", "individual_leopard_summary.csv"],
            ["Cheetah", "(individual identifier)", "individual_cheetah_summary.csv"],
        ],
        [2*cm, 4*cm, W - 6*cm],
    ),
    sp(6),
    h2("8.4  Sighting maps (all species)"),
    p("Each sighting map follows the same pipeline: "
      "exclude_geom_outliers (z=3) → drop_null_geometry → "
      "apply_color_map (herd_composition or equivalent field, tab20 → colors) → "
      "create_scatterplot_layer → combine with conservancy boundaries + "
      "parcels + text labels → draw_map (global_zoom_value, max_zoom: 15) → "
      "persist HTML → html_to_png (scale: 2.0, wait: 40 s)."),
    sp(6),
    h2("8.5  Elephant and buffalo herd-size map and bar chart"),
    p("In addition to the standard sighting map, elephant and buffalo each produce:"),
    make_table(
        [
            ["Output", "Task", "Detail"],
            ["Herd-size bar chart",
             "draw_bar_chart",
             "bin_columns (7 bins, suffix: bins) → categorize_bins → "
             "draw_bar_chart (category: herd_sizebins, agg: count(id), "
             "marker_color: lightsteelblue) → persist HTML → html_to_png."],
            ["Herd-size map",
             "draw_map",
             "drop_null_values → exclude_geom_outliers → drop_null_geometry → "
             "clean_dataframe_index → apply_color_map (herd_sizebins_sort, Blues) → "
             "create_scatterplot_layer (get_radius: herd_size, radius_units: pixels, "
             "radius_scale: 0.43) → combine with conservancy boundaries + "
             "parcels + text labels → draw_map → persist HTML → html_to_png."],
        ],
        [3*cm, 2.5*cm, W - 5.5*cm],
    ),
    make_table(
        [
            ["Species", "Bar chart filename", "Herd-size map filename"],
            ["Elephant", "elephant_herd_size_bar_chart.html/.png",
             "elephant_herd_types_map.html/.png"],
            ["Buffalo",  "buffalo_herd_size_bar_chart.html/.png",
             "buffalo_herd_types_map.html/.png"],
        ],
        [2.5*cm, 5*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("8.6  Wildlife incidents"),
    p("Task: <b>filter_row_values</b> on events_temporal for event types: "
      "snare_rep, fire_rep, wildlife_injury_rep, wildlife_treatment_rep, "
      "wildlife_carcass_rep. Three CSV outputs are produced:"),
    make_table(
        [
            ["CSV filename", "Description"],
            ["wildlife_events_recorded.csv",
             "Summary of wildlife incident event counts"],
            ["wildlife_incidents_summary_table.csv",
             "Incident counts broken down by event type"],
            ["wildlife_incidents_recorded_by_date.csv",
             "Incident counts grouped by date"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    p("A map of all wildlife incident locations is also produced: "
      "exclude_geom_outliers → drop_null_geometry → apply_color_map → "
      "create_scatterplot_layer → draw_map → persist as "
      "<b>wildlife_incidents_map.html/.png</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. SECTION 5 — PATROL REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Section 5 — Patrol Report"),
    hr(),
    p("The patrol section derives trajectory data from <b>patrol_info</b> events "
      "in events_temporal, rather than from a direct patrol observation fetch. "
      "It produces event count summaries, patrol purpose statistics, trajectory "
      "files, patrol effort CSVs, three trajectory maps, a patrol coverage grid "
      "map, and a patrol occupancy table."),
    sp(6),
    h2("9.1  Event counts (all event types)"),
    p("Before the patrol-specific pipeline, two cross-section event count tables "
      "are produced from the filtered events_temporal (excluding "
      "distancecountwildlife_rep, distancecountpatrol_rep, airstrip_operations, "
      "and silence_source_rep):"),
    make_table(
        [
            ["CSV filename", "Group-by", "Description"],
            ["total_events_recorded_by_date.csv",
             "date", "Unique event count per date with a Total row"],
            ["total_events_recorded_by_type.csv",
             "date + event_type", "Unique event count per date per event type"],
        ],
        [5*cm, 2.5*cm, W - 7.5*cm],
    ),
    p("A bar chart of total events is also drawn and saved as "
      "<b>total_events_recorded.html/.png</b>."),
    sp(6),
    h2("9.2  Patrol purpose summary"),
    p("Task: filter events_temporal for event_type == <b>patrol_info</b>. "
      "The event_details JSON is normalised (without process_events_details — "
      "raw key names are used) and columns are renamed:"),
    make_table(
        [
            ["Raw key", "Renamed to"],
            ["event_details__patrolinfomation_participants", "participants"],
            ["event_details__patrolinfomation_patrolpurpose", "purpose"],
            ["event_details__patrolinfomation_personwhoauthorised", "authorized_by"],
            ["event_details__patrolinfomation_transporttype", "transport_type"],
            ["patrols", "patrol_id"],
        ],
        [7*cm, W - 7*cm],
    ),
    p("The purpose summary table groups by <b>purpose</b> and aggregates "
      "nunique(id) → no_of_patrols and sum(dist_meters, m→km) → distance_km. "
      "Saved as <b>patrol_purpose_summary.csv</b> (with a Total row)."),
    sp(6),
    h2("9.3  Patrol observations and relocations"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_null_patrols",
             "Remove rows with null patrol_id."],
            ["2", "replace_missing_with_label",
             "Fill null transport_type values with 'unspecified'."],
            ["3", "explode_multiple_columns",
             "Explode patrol_id and participants lists into rows."],
            ["4", "get_patrol_values",
             "Fetch full patrol records from EarthRanger by patrol_id "
             "(batch_size: 15)."],
            ["5", "custom_get_patrol_observations_from_patrols_df",
             "Fetch GPS observations for each patrol "
             "(include_patrol_details: true, raise_on_empty: true, "
             "sub_page_size: 150)."],
            ["6", "merge_dataframes",
             "Left-join observations with patrol info on patrol_id."],
            ["7", "process_relocations",
             "Convert observations to relocations. Columns retained include: "
             "patrol_id, patrol_title, patrol_serial_number, patrol_start/end_time, "
             "patrol_type, patrol_status, patrol_subject, patrol_type__value, "
             "participants, purpose, transport_type. "
             "Junk coordinates filtered: (180,90), (0,0), (1,1)."],
            ["8", "persist_df",
             "Save as <b>patrol_relocations.geoparquet</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.4  Trajectory building"),
    p("Relocations are filtered into three transport type sub-groups and "
      "independently converted to trajectories:"),
    make_table(
        [
            ["Sub-group", "filter value", "Trajectory segment filter"],
            ["Foot patrols",    "foot",       "max_length: 5 000 m, max_time: 14 400 s, "
                                              "speed: 0.5–9 km/h"],
            ["Vehicle patrols", "vehicle",    "max_length: 5 000 m, max_time: 18 000 s, "
                                              "speed: 10–100 km/h"],
            ["Motorbike patrols","motorbike",  "max_length: 5 000 m, max_time: 18 000 s, "
                                              "speed: 5–120 km/h"],
        ],
        [3*cm, 2.5*cm, W - 5.5*cm],
    ),
    note("Each sub-group runs relocations_to_trajectory independently, producing "
         "separate trajectory DataFrames. A combined trajectory DataFrame is also "
         "assembled (rename_combined_trajs) for the patrol coverage analysis."),
    sp(6),
    h2("9.5  Patrol effort CSVs"),
    p("Each patrol type produces a metrics summary table "
      "(patrol_type_value, no_of_patrols, distance_km, duration_hrs, average_speed) "
      "with a Total row:"),
    make_table(
        [
            ["CSV filename", "Source"],
            ["foot_patrol_efforts.csv",       "foot patrol trajectories"],
            ["vehicle_patrol_efforts.csv",    "vehicle patrol trajectories"],
            ["motorbike_patrol_efforts.csv",  "motorbike patrol trajectories"],
            ["overall_patrol_efforts.csv",    "combined trajectories — all patrol types together"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("9.6  Patrol trajectory maps"),
    p("Three GeoJSON-based trajectory maps are produced using "
      "<b>create_geojson_layer</b>. Each map: apply_color_map (patrol_type_value, "
      "tab20) → filter_columns → gdf_to_geojson → create_geojson_layer → "
      "combine with conservancy boundaries + parcels + text labels → draw_map → "
      "rewrite_file_urls_for_screenshots → persist HTML → html_to_png."),
    make_table(
        [
            ["Map", "GeoJSON filename", "HTML filename"],
            ["Foot patrols",    "foot_patrol_trajectories.geojson",
             "foot_patrols_map.html/.png"],
            ["Vehicle patrols", "vehicle_patrol_trajectories.geojson",
             "vehicle_patrols_map.html/.png"],
            ["Motorbike patrols","motor_patrol_trajectories.geojson",
             "motorbike_patrols_map.html/.png"],
        ],
        [3*cm, 4.5*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("9.7  Patrol coverage map and occupancy"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "create_patrol_coverage_grid",
             "Build a 1 000 m grid and count unique patrol visits per cell "
             "from the combined trajectories."],
            ["2", "apply_classification",
             "Classify unique_patrol_count into 5 equal-interval bins "
             "→ density_bins (label_ranges: false, label_decimals: 1)."],
            ["3", "apply_color_map",
             "Apply RdYlGn_r colormap to density_bins → density_colors."],
            ["4", "create_geojson_layer + draw_map",
             "Render grid as a filled polygon layer → draw_map → "
             "persist as <b>patrol_coverage_map.html/.png</b>."],
            ["5", "compute_occupancy",
             "Compute occupancy percentage of the conservancy area covered "
             "by patrol grid cells (crs: epsg:4326)."],
            ["6", "round_values",
             "Round occupancy_percentage to 2 decimal places."],
            ["7", "persist_df",
             "Save as <b>patrol_coverage.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. REPORT GENERATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Report Generation"),
    hr(),
    p("The workflow concludes by generating a populated Word report using "
      "<b>generate_mnc_report</b> (from ecoscope-workflows-ext-mnc)."),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",           "generate_mnc_report"],
            ["template_path",  "mara_north_event_template.docx (fetched from Dropbox)"],
            ["output_dir",     "ECOSCOPE_WORKFLOWS_RESULTS"],
            ["generated_by",   "Ecoscope"],
            ["validate_images","true"],
            ["time_period",    "from time_range"],
            ["filename",       "overall_report.docx"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("The generate_mnc_report task auto-discovers PNG outputs in "
         "ECOSCOPE_WORKFLOWS_RESULTS and populates the template placeholders. "
         "With validate_images: true, the task will raise if expected PNG files "
         "are missing."),
    sp(6),
    p("A <b>gather_dashboard</b> task also runs at the end, packaging the "
      "workflow details, time range, and groupers. The widgets list is empty."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    h2("11.1  Weather"),
    make_table(
        [
            ["File", "Description"],
            ["weather_summary_table.csv",
             "Daily aggregated weather: precipitation (sum), temperature (mean), "
             "wind speed (mean), wind gusts (max), soil temperature (mean), "
             "relative humidity (mean), atmospheric pressure (mean)"],
            ["precipitation_readings_over_time.html/.png",
             "Precipitation line chart per weather station"],
            ["temperature_readings_over_time.html/.png",
             "Temperature line chart per weather station"],
            ["wind_speed_readings_over_time.html/.png",
             "Wind speed line chart"],
            ["wind_gusts_readings_over_time.html/.png",
             "Wind gusts line chart"],
            ["soil_temperature_readings_over_time.html/.png",
             "Soil temperature line chart"],
            ["relative_humidity_readings_over_time.html/.png",
             "Relative humidity line chart"],
            ["atmospheric_pressure_readings_over_time.html/.png",
             "Atmospheric pressure line chart"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("11.2  Logistics"),
    make_table(
        [
            ["File", "Description"],
            ["balloon_landing_summary_table.csv",
             "Passenger records by balloon company and lodge"],
            ["airstrip_operations_summary_table.csv",
             "Total clients per camp/lodge pivoted by arrival/departure"],
            ["airstrip_maintenance_summary_table.csv",
             "Dated log of airstrip maintenance activity types"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("11.3  Livestock"),
    make_table(
        [
            ["File", "Description"],
            ["mobile_boma_movement_summary_table.csv",
             "Daily unique boma event count with a Total row"],
            ["total_cattle_count_summary_table.csv",
             "Cattle counts per zone (zone_1, zone_2_3, zone_4, total_count) per date"],
            ["total_livestock_predation_summary_table.csv",
             "Daily unique predation event count with a Total row"],
            ["livestock_predation_summary_table.csv",
             "Predation records by species, suspected predator, and total animals affected"],
            ["boma_movement_map.html/.png",
             "Mobile boma locations on MNC grazing zones and parcels, coloured by event type"],
            ["livestock_predation_events.html/.png",
             "Predation incident locations, coloured by livestock species"],
            ["illegal_grazing_map.html/.png",
             "Illegal grazing incidents on MNC grazing zones, coloured by event type"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("11.4  Wildlife"),
    make_table(
        [
            ["File", "Description"],
            ["total_elephants_events_recorded.csv",
             "Daily elephant sighting count with Total row"],
            ["total_buffalo_events_recorded.csv",
             "Daily buffalo sighting count with Total row"],
            ["total_rhino_events_recorded.csv",
             "Daily rhino sighting count with Total row"],
            ["total_lion_events_recorded.csv",
             "Daily lion sighting count with Total row"],
            ["total_leopard_events_recorded.csv",
             "Daily leopard sighting count with Total row"],
            ["total_cheetah_events_recorded.csv",
             "Daily cheetah sighting count with Total row"],
            ["individual_lions_summary.csv",
             "Lion sighting count grouped by pride"],
            ["individual_leopard_summary.csv",
             "Leopard sighting count grouped by individual identifier"],
            ["individual_cheetah_summary.csv",
             "Cheetah sighting count grouped by individual identifier"],
            ["wildlife_events_recorded.csv",
             "Overall wildlife incident event counts"],
            ["wildlife_incidents_summary_table.csv",
             "Incident counts by event type"],
            ["wildlife_incidents_recorded_by_date.csv",
             "Incident counts by date"],
            ["elephant_sightings_events.html/.png",
             "Elephant sighting map, coloured by herd_composition (tab20)"],
            ["elephant_herd_size_bar_chart.html/.png",
             "Elephant group-size frequency bar chart"],
            ["elephant_herd_types_map.html/.png",
             "Elephant sighting map with points scaled by herd_size (Blues)"],
            ["buffalo_sightings_events.html/.png",
             "Buffalo sighting map, coloured by herd_composition"],
            ["buffalo_herd_size_bar_chart.html/.png",
             "Buffalo group-size frequency bar chart"],
            ["buffalo_herd_types_map.html/.png",
             "Buffalo sighting map with points scaled by herd_size"],
            ["rhino_sightings_events.html/.png",
             "Rhino sighting map"],
            ["lion_sightings_events.html/.png",
             "Lion sighting map, coloured by pride"],
            ["leopard_sightings_events.html/.png",
             "Leopard sighting map"],
            ["cheetah_sightings_events.html/.png",
             "Cheetah sighting map"],
            ["giraffe_sightings_events.html/.png",
             "Giraffe sighting map"],
            ["hartebeest_sightings_events.html/.png",
             "Hartebeest sighting map"],
            ["wildlife_incidents_map.html/.png",
             "Wildlife incident locations map"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("11.5  Patrol"),
    make_table(
        [
            ["File", "Description"],
            ["total_events_recorded_by_date.csv",
             "Daily unique event count (all types, excl. 4 excluded types) with Total row"],
            ["total_events_recorded_by_type.csv",
             "Daily unique event count per event type"],
            ["total_events_recorded.html/.png",
             "Total events bar chart"],
            ["patrol_purpose_summary.csv",
             "Patrol count and distance by purpose with Total row"],
            ["patrol_relocations.geoparquet",
             "Cleaned GPS relocations for all patrol types"],
            ["foot_patrol_efforts.csv",
             "Foot patrol metrics (patrols, distance km, duration hrs, avg speed) by type"],
            ["vehicle_patrol_efforts.csv",
             "Vehicle patrol metrics by type"],
            ["motorbike_patrol_efforts.csv",
             "Motorbike patrol metrics by type"],
            ["overall_patrol_efforts.csv",
             "Combined patrol metrics across all types with Total row"],
            ["foot_patrol_trajectories.geojson",
             "Foot patrol trajectory segments with colour column"],
            ["vehicle_patrol_trajectories.geojson",
             "Vehicle patrol trajectory segments with colour column"],
            ["motor_patrol_trajectories.geojson",
             "Motorbike patrol trajectory segments with colour column"],
            ["patrol_trajectories.geojson",
             "Combined trajectory segments (all patrol types)"],
            ["foot_patrols_map.html/.png",
             "Foot patrol trajectories map, coloured by patrol type"],
            ["vehicle_patrols_map.html/.png",
             "Vehicle patrol trajectories map, coloured by patrol type"],
            ["motorbike_patrols_map.html/.png",
             "Motorbike patrol trajectories map, coloured by patrol type"],
            ["patrol_coverage_map.html/.png",
             "1 000 m patrol coverage grid, classified by visit count (RdYlGn_r)"],
            ["patrol_coverage.csv",
             "Patrol occupancy percentage per conservancy region"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("11.6  Report"),
    make_table(
        [
            ["File", "Description"],
            ["mara_north_event_template.docx",
             "Word template downloaded from Dropbox (not an output — input)"],
            ["overall_report.docx",
             "Populated Word report generated from the template"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Workflow Execution Logic"),
    hr(),
    h2("12.1  Per-task skip conditions"),
    p("This workflow does <b>not</b> use a global <b>task-instance-defaults</b> "
      "block. Every task from event retrieval onwards carries its own explicit "
      "skipif block:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",
             "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped",
             "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Because skip conditions are per-task rather than global, each section "
         "propagates skips independently. For example, if no balloon_landing events "
         "are returned, only the balloon branch skips; all other sections continue."),
    sp(6),
    h2("12.2  Two independent data sources"),
    p("The workflow has two distinct entry points that run in parallel:"),
    make_table(
        [
            ["Entry point", "Task", "Feeds sections"],
            ["Weather observations",
             "get_subjectgroup_observations (subject_group: ER2ER - From GMMF)",
             "Section 1 — Weather only"],
            ["All event records",
             "get_events (event_types: [], fetch all)",
             "Sections 2–5 — Logistics, Livestock, Wildlife, Patrol"],
        ],
        [3.5*cm, 5*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("12.3  No mapvalues or fan-out"),
    p("This workflow processes all records as a single batch. There is no "
      "<b>mapvalues</b>, <b>split_groups</b>, or <b>zip_groupbykey</b> directive — "
      "every task runs exactly once per workflow execution."),
    sp(6),
    h2("12.4  GeoJSON trajectories and URL rewriting"),
    p("Patrol trajectory maps use <b>create_geojson_layer</b> with an inline "
      "GeoJSON data_url reference. Before HTML-to-PNG conversion, "
      "<b>rewrite_file_urls_for_screenshots</b> replaces the file:// URL in the "
      "rendered HTML with a locally-served path so the headless browser can load "
      "the GeoJSON. All three patrol maps use <b>serve_local_files: true</b> in "
      "their html_to_png config."),
    sp(6),
    h2("12.5  HTML-to-PNG conversion settings"),
    make_table(
        [
            ["Group", "device_scale_factor", "wait_for_timeout", "max_concurrent_pages"],
            ["Weather charts (batch)",  "2.0", "15 ms",    "5"],
            ["Livestock / wildlife maps","2.0", "40 000 ms","1"],
            ["Elephant bar chart",      "2.0", "10 ms",    "1"],
            ["Patrol maps",             "2.0", "40 000 ms","1"],
        ],
        [3.5*cm, 3*cm, 3*cm, W - 9.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.18.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.45.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.19.*"],
            ["ecoscope-workflows-ext-mep",     "0.0.14.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.9.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
