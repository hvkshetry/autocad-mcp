# AutoCAD MCP Further Improvements
## Wastewater Engineering Focus for AutoCAD LT

### Executive Summary
This document outlines strategic improvements to transform the AutoCAD MCP into a specialized wastewater engineering tool, working within AutoCAD LT 2024+ limitations while leveraging the CAD Tools Online P&ID Symbols Library (ISA 5.1-2009 standard). The focus is on creating efficient workflows for wastewater treatment plant design, collection system modeling, and P&ID creation.

---

## 1. Core Architecture Enhancements for Wastewater

### 1.1 Symbol Library Integration - Complete CTO Library Access
**Strategy**: Expose all CAD Tools Online P&ID symbols (C:\PIDv4-CTO) through MCP tools for autonomous P&ID creation.

#### Block Library Structure
```lisp
;; Complete CTO library mapping for MCP exposure
(defun initialize-cto-library ()
  (setq *cto-categories* '(
    ("ACTUATORS" . (
      ("Bellows Spring" . "ACT-BELLOWS_SPRING")
      ("Electrohydraulic" . "ACT-ELECTROHYDRAULIC")
      ("Handle" . "ACT-HANDLE")
      ("Linear Piston" . "ACT-LINEAR_PISTON")
      ("Linear Piston Positioner" . "ACT-LINEAR_PISTON_POSITIONER")
      ("Motor" . "ACT-MOTOR")
      ("Pilot Relief" . "ACT-PILOT_RELIEF")
      ("Pressure Balance" . "ACT-PRESSURE_BALANCE")
      ("Relief" . "ACT-RELIEF")
      ("Rotary Piston" . "ACT-ROTARY_PISTON")
      ("Rotary Piston Positioner" . "ACT-ROTARY_PISTON_POSITIONER")
      ("Solenoid" . "ACT-SOLENOID")
      ("Spring Diaphragm" . "ACT-SPRING_DIAPHRAGM")
      ("Spring Diaphragm Positioner" . "ACT-SPRINGDIA_POSITIONER")))
    
    ("ANNOTATION" . (
      ("Drawing Process Connect Left" . "ANNOT-DWG_PROCESS_CONNECT-LEFT-2")
      ("Drawing Signal Connect Left" . "ANNOT-DWG_SIGNAL_CONNECT-LEFT")
      ("Equipment Description" . "ANNOT-EQUIP_DESCR")
      ("Equipment Tag" . "ANNOT-EQUIP_TAG")
      ("Flow Arrow" . "ANNOT-FLOWARROW")
      ("Line Number" . "ANNOT-LINE_NUMBER")
      ("Pipe Spec Break" . "ANNOT-PIPE_SPEC_BREAK")
      ("Revision Triangle" . "ANNOT-REV_TRIANGLE")
      ("Slope Left" . "ANNOT-SLOPE_LEFT")
      ("Slope Right" . "ANNOT-SLOPE_RIGHT")))
    
    ("BORDERS" . (
      ;; Border templates for drawing sheets
    ))
    
    ("ELECTRICAL" . (
      ("Battery" . "ELEC-BATTERY")
      ("Circuit Breaker Single" . "ELEC-CIRC_BRKR_SINGLE_POLE")
      ("Circuit Breaker Three" . "ELEC-CIRC_BRKR_THREE_POLE")
      ("Differential Pressure Switch" . "ELEC-DIFF_PRESS_SW_ACT")
      ("Flow Switch" . "ELEC-FLOW_SW_ACT")
      ("Ground" . "ELEC-GROUND")
      ("Interlock" . "ELEC-INTERLOCK")
      ("Level Switch" . "ELEC-LIQ_LEV_SW_ACT")
      ("Motor Starter" . "ELEC-MOTOR")
      ("Pilot Light" . "ELEC-PILOT_LIGHT")
      ("Pressure Switch" . "ELEC-PRESS_SW_ACT")
      ("Temperature Switch" . "ELEC-TEMP_SW_ACT")
      ("VFD" . "ELEC-VFD")))
    
    ("EQUIPMENT" . (
      ("Air Compressor" . "EQUIP-AIR_COMP")
      ("Air Dryer" . "EQUIP-AIR_DRYER")
      ("Air Separator" . "EQUIP-AIR_SEP")
      ("Belt Skimmer" . "EQUIP-BELT_SKIMMER")
      ("Bin" . "EQUIP-BIN")
      ("Centrifuge" . "EQUIP-CENTRIFUGE")
      ("Clarifier" . "EQUIP-CLARIFIER")
      ("Conveyor Belt" . "EQUIP-CONV_BELT")
      ("Conveyor Screw" . "EQUIP-CONV_SCREW")
      ("Cyclone" . "EQUIP-CYCLONE")
      ("Drum" . "EQUIP-DRUM")
      ("Filter" . "EQUIP-FILTER")
      ("Filter Press" . "EQUIP-FILTER_PRESS")
      ("Gas Scrubber" . "EQUIP-GAS_SCRUBBER")
      ("Heat Exchanger Generic" . "EQUIP-HEAT_EXCH-GENERIC")
      ("Heat Exchanger Plate" . "EQUIP-HEAT_EXCH-PLATE_FRAME")
      ("Inline Mixer" . "EQUIP-INLINEMIXER")
      ("Motor" . "EQUIP-MOTOR")
      ("Rotary Screen" . "EQUIP-ROTARY_SCREEN")
      ("Screen Bar" . "EQUIP-SCREENBAR")
      ("Strainer Single" . "EQUIP-SINGLE_STRAINER")
      ("Strainer Duplex" . "EQUIP-DUPLEX_STRAINER")))
    
    ("FUNCTION" . (
      ("Analog Signal Generator" . "FUNCT-ANALOGSIGGENERATOR")
      ("Average" . "FUNCT-AVERAGE")
      ("Conversion" . "FUNCT-CONVERSION")
      ("High Limit" . "FUNCT-HIGHLIMIT")
      ("High Signal Select" . "FUNCT-HIGHSIGSELECT")
      ("Integral" . "FUNCT-INTEGRALa")
      ("Low Limit" . "FUNCT-LOWLIMIT")
      ("Low Signal Select" . "FUNCT-LOWSIGSELECT")
      ("Proportion" . "FUNCT-PROPORTION_P")
      ("Signal Transfer" . "FUNCT-SIGNALTRANSFER")
      ("Summation" . "FUNCT-SUMMATION")))
    
    ("INSTRUMENTS" . (
      ("Board Plugin Point" . "INST-BOARDPLUGINPT")
      ("Computer Field Access" . "INST-COMP-FLDACCESS")
      ("Discrete Field Access" . "INST-DISC-FLDACCESS")
      ("Flanged Connection" . "INST-FLGD_CONN_PT")
      ("Interlock" . "INST-INTERLOCK")
      ("PLC Field Access" . "INST-PLC-FLDACCESS")
      ("Shared Display" . "INST-SHARED-FLDACCESS")
      ("Socket Weld Connection" . "INST-SW_CONN_PT")
      ("Threaded Connection" . "INST-THD_CONN_PT")
      ("Weld Connection" . "INST-WELD_CONN_PT")))
    
    ("PIPING" . (
      ("Air Filter" . "PIPING-AIR_FILTER")
      ("Air Filter Regulator" . "PIPING-AIR_FILT_REG")
      ("Diaphragm Seal" . "PIPING-DIAPHRAGM_SEAL")
      ("Drain" . "PIPING-DRAIN")
      ("Expansion Joint" . "PIPING-EXPANSION_JOINT")
      ("Flange" . "PIPING-FLANGE")
      ("Flexible Hose" . "PIPING-FLEX_HOSE")
      ("Insulation" . "PIPING-INSULATION")
      ("Line Break" . "PIPING-LINE_BREAK_HVY")
      ("Pipe Cap" . "PIPING-PIPE_CAP1")
      ("Reducer Concentric" . "PIPING-REDUCER_CONC")
      ("Reducer Eccentric" . "PIPING-REDUCER_ECC")
      ("Rupture Disc" . "PIPING-RUPTURE_DISC")
      ("Steam Trap" . "PIPING-STEAM_TRAP")
      ("Strainer" . "PIPING-STRAINER")
      ("Union" . "PIPING-UNION")))
    
    ("PRIMARY_ELEMENTS" . (
      ("Coriolis Flow" . "PRIMELEM-CORIOLLIS_FLOWMETER")
      ("Displacer" . "PRIMELEM-DISPLACER")
      ("Float" . "PRIMELEM-FLOAT")
      ("Flow Nozzle" . "PRIMELEM-FLOW_NOZZLE")
      ("Magnetic Flow" . "PRIMELEM-MAGNETIC_FLOWMETER")
      ("Orifice Plate" . "PRIMELEM-ORIFICE_PLATE")
      ("Pitot Tube" . "PRIMELEM-PITOT_TUBE")
      ("Turbine Flow" . "PRIMELEM-TURBINE_FLOWMETER")
      ("Vortex Flow" . "PRIMELEM-VORTEX_SHEDDING_FLOWMETER")))
    
    ("PUMPS-BLOWERS" . (
      ("Blower Centrifugal" . "BLOWER-CENTRIFUGAL")
      ("Blower Rotary" . "BLOWER-ROTARY")
      ("Compressor Centrifugal" . "COMP-CENTRIFUGAL")
      ("Pump Centrifugal 1" . "PUMP-CENTRIF1")
      ("Pump Centrifugal 2" . "PUMP-CENTRIF2")
      ("Pump Diaphragm" . "PUMP-DIAPHRAGM")
      ("Pump Gear" . "PUMP-GEAR")
      ("Pump Metering" . "PUMP-METERING")
      ("Pump Progressive Cavity" . "PUMP-PROGRESSIVE_CAVITY")
      ("Pump Reciprocating" . "PUMP-RECIPROCATING")
      ("Pump Screw" . "PUMP-SCREW")
      ("Pump Submersible" . "PUMP-SUBMERSIBLE")
      ("Pump Sump" . "PUMP-SUMP")
      ("Pump Vertical Turbine" . "PUMP-VERTICAL_TURBINE")))
    
    ("REGULATORS" . (
      ("Automatic Regulator" . "REG-AUTOMATIC")
      ("Back Pressure External" . "REG-BACKPRESSURE_EXTERNAL_TAP")
      ("Back Pressure Internal" . "REG-BACKPRESSURE_INTERNAL_TAP")
      ("Constant Flow" . "REG-CONSTANT_FLOW")
      ("Level Regulator" . "REG-LEVEL_REGULATOR")
      ("Pressure Reducing" . "REG-PRESSURE_REDUCING_RELIEF_GAUGE")
      ("Pressure Relief" . "REG-PRESSURE_RELIEF")
      ("Temperature Regulator" . "REG-TEMPERATURE_REGULATOR")
      ("Vacuum Relief" . "REG-VACUUM_RELIEF")))
    
    ("TANKS" . (
      ("55 Gallon Drum" . "TANK-55GALDRUM")
      ("Cone Bottom Dome" . "TANK-CONE_BOTTOM_DOME")
      ("Cone Bottom Open" . "TANK-CONE_BOTTOM_OPEN")
      ("Diffuser" . "TANK-DIFFUSER")
      ("Elevated Tank" . "TANK-ELEVATED")
      ("Floating Lid" . "TANK-FLOATING_LID")
      ("Horizontal Tank" . "TANK-HORIZONTAL")
      ("Propeller Aerator" . "TANK-PROP_AERATOR")
      ("Propeller Agitator" . "TANK-PROP_AGITATOR")
      ("Sparge Aerator" . "TANK-SPARGE_AERATOR")
      ("Turbine Agitator" . "TANK-TURBINE_AGITATOR")
      ("Vertical Dome" . "TANK-VERTICAL_DOME")
      ("Vertical Open" . "TANK-VERTICAL_OPEN")))
    
    ("VALVES" . (
      ("3-Way Valve" . "VA-3WAY")
      ("3-Way Flanged" . "VA-3WAY-FLG")
      ("4-Way Valve" . "VA-4WAY")
      ("Angle Valve" . "VA-ANGLE")
      ("Angle Flanged" . "VA-ANGLE-FLG")
      ("Ball Valve" . "VA-BALL")
      ("Ball Flanged" . "VA-BALL-FLG")
      ("Butterfly Valve" . "VA-BUTTERFLY")
      ("Butterfly Flanged" . "VA-BUTTERFLY-FLG")
      ("Check Valve" . "VA-CHECK")
      ("Check Flanged" . "VA-CHECK-FLG")
      ("Diaphragm Valve" . "VA-DIAPHRAGM")
      ("Gate Valve" . "VA-GATE")
      ("Gate Flanged" . "VA-GATE-FLG")
      ("Globe Valve" . "VA-GLOBE")
      ("Globe Flanged" . "VA-GLOBE-FLG")
      ("Knife Gate" . "VA-KNIFEGATE")
      ("Needle Valve" . "VA-NEEDLE")
      ("Pinch Valve" . "VA-PINCH")
      ("Plug Valve" . "VA-PLUG")
      ("Plug Flanged" . "VA-PLUG-FLG")))
  ))
)

;; MCP Tool: Universal block insertion with attributes
@autocad_mcp.tool()
async def insert_pid_symbol(category: str, symbol_name: str, x: float, y: float, 
                           scale: float = 1.0, rotation: float = 0.0,
                           attributes: Optional[Dict[str, str]] = None) -> str:
    """
    Insert any P&ID symbol from the CTO library with optional attributes.
    
    Args:
        category: Category name (e.g., "VALVES", "EQUIPMENT", "PUMPS-BLOWERS")
        symbol_name: Symbol filename without extension (e.g., "VA-GATE", "EQUIP-CLARIFIER")
        x, y: Insertion point coordinates
        scale: Scale factor (default 1.0)
        rotation: Rotation in degrees (default 0.0)
        attributes: Dictionary of attribute tags and values
    """
    path = f"C:\\PIDv4-CTO\\{category}\\{symbol_name}.dwg"
    
    # Load block if not already loaded
    cmd = f'(if (not (tblsearch "BLOCK" "{symbol_name}")) ' + \
          f'(command "_.-INSERT" "{path}" nil))'
    execute_lisp_command(cmd)
    
    # Insert block with entmake for precise control
    lisp_code = f'''
    (progn
      (setq ent-list (list
        '(0 . "INSERT")
        '(100 . "AcDbEntity")
        '(8 . "0")  ; Default layer, will be updated by block
        '(100 . "AcDbBlockReference")
        (cons 2 "{symbol_name}")
        (cons 10 (list {x} {y} 0.0))
        (cons 41 {scale})
        (cons 42 {scale})
        (cons 43 {scale})
        (cons 50 (* {rotation} (/ pi 180.0)))
      ))
      (setq block-ent (entmake ent-list))
    '''
    
    # Add attributes if provided
    if attributes:
        for tag, value in attributes.items():
            lisp_code += f'''
      (entmake (list
        '(0 . "ATTRIB")
        '(100 . "AcDbEntity")
        '(100 . "AcDbText")
        '(100 . "AcDbAttribute")
        (cons 2 "{tag}")
        (cons 1 "{value}")
        (cons 10 (list {x} {y} 0.0))
        '(40 . 2.5)  ; Text height
        '(50 . 0.0)  ; Text rotation
      ))
    '''
        lisp_code += '''
      (entmake '((0 . "SEQEND")))
    '''
    
    lisp_code += '''
      (princ "Symbol inserted successfully")
    )
    '''
    
    success, message = execute_lisp_command(lisp_code)
    return f"Inserted {symbol_name} at ({x},{y})" if success else message

;; MCP Tool: Intelligent P&ID builder from description
@autocad_mcp.tool()
async def build_pid_from_description(process_description: str) -> str:
    """
    Autonomously create a P&ID from a natural language description.
    
    Example: "Create a wastewater treatment process with screening, 
              primary clarification, aeration basin, secondary clarifier, 
              and UV disinfection"
    """
    # Parse description and generate P&ID
    components = parse_process_description(process_description)
    layout = calculate_pid_layout(components)
    
    for component in components:
        insert_pid_symbol(
            category=component['category'],
            symbol_name=component['symbol'],
            x=component['x'],
            y=component['y'],
            attributes={
                'TAG': component['tag'],
                'DESCRIPTION': component['description'],
                'SIZE': component.get('size', ''),
                'CAPACITY': component.get('capacity', '')
            }
        )
    
    # Connect with piping
    create_process_connections(components)
    
    # Add instrumentation
    add_standard_instrumentation(components)
    
    return f"P&ID created with {len(components)} components"

;; Helper function to get all available symbols
(defun get-cto-symbol-list (category / path files)
  (setq path (strcat "C:\\PIDv4-CTO\\" category "\\"))
  (setq files (vl-directory-files path "*.dwg" 1))
  (mapcar '(lambda (f) (vl-filename-base f)) files)
)

;; Smart symbol search
(defun find-symbol-by-keyword (keyword / matches)
  (setq matches '())
  (foreach cat (mapcar 'car *cto-categories*)
    (foreach sym (get-cto-symbol-list cat)
      (if (vl-string-search (strcase keyword) (strcase sym))
        (setq matches (cons (cons cat sym) matches)))))
  matches
)
```

### 1.2 Layer Management System
**Purpose**: Standardized layer structure for wastewater projects.

```lisp
(defun c:setup-ww-layers ()
  ;; Create standard wastewater layers
  (create-layer "WW-PROCESS-EQUIPMENT" "6" "CONTINUOUS" "0.35mm")
  (create-layer "WW-PROCESS-PIPING" "4" "CONTINUOUS" "0.50mm")
  (create-layer "WW-SLUDGE-PIPING" "30" "DASHED" "0.35mm")
  (create-layer "WW-CHEMICAL-PIPING" "1" "PHANTOM" "0.25mm")
  (create-layer "WW-INSTRUMENTATION" "5" "CONTINUOUS" "0.25mm")
  (create-layer "WW-ELECTRICAL" "7" "CONTINUOUS" "0.25mm")
  (create-layer "WW-CONCRETE" "8" "CONTINUOUS" "0.50mm")
  (create-layer "WW-ANNOTATION" "7" "CONTINUOUS" "0.25mm")
  (princ "\nWastewater layers created successfully.")
)
```

---

 