# HA-Ventoxx-HRV: Home Assistant Integration for Ventoxx HRV

[![Example of card on the Dashboard](images/Ventoxx_Dashboard.png)](images/Ventoxx_Dashboard.png)
[![Example of card on the Dashboard](images/Ventoxx_integration_slider.png)](images/Ventoxx_integration_slider.png)

A fully local, custom integration for Home Assistant to natively control Ventoxx Harmony Smart Heat Recovery Ventilation units via Wi-Fi.

**🎉 NEW UPDATE:** This integration is now a **100% native Python custom component!** You no longer need to manually copy YAML template sensors or REST commands. The integration now automatically creates standard Home Assistant Fan entities and dynamic Status Sensors for you.

## Features
* **Native Fan Control:** Turn your Ventoxx on/off, set speeds (1-3), and control direction (Intake/Exhaust) using standard Home Assistant UI sliders and buttons.
* **Presets Supported:** Supports `Normal`, `Heat Recovery`, `Boost`, and `Night` modes natively.
* **Automatic Status Sensors:** Automatically generates a human-readable text sensor (e.g., `HRV Speed 2 - Exhaust`) with dynamic icons for easy dashboard viewing. No YAML templates required!
* **Fully Local:** Communicates directly with the ESP32 inside the Ventoxx unit over your local Wi-Fi without any cloud dependency.

## Installation

### Method 1: HACS (Recommended)
1. Open HACS in your Home Assistant instance.
2. Click the 3 dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository and select **Integration** as the category.
4. Click **Install** on the HA-Ventoxx-HRV integration.
5. Restart Home Assistant.
6. Go to **Settings > Devices & Services > Add Integration** and search for Ventoxx.

### Method 2: Manual
1. Download this repository.
2. Copy the `custom_components/ventoxx` folder into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration** and search for Ventoxx.

---

## Example Scripts (Dual-Unit Synchronization)

Because this integration now uses native Home Assistant fan commands, you can easily script complex behaviors without dealing with raw hardware codes. 

If you have two Ventoxx units (e.g., Kitchen and Living Room), add these examples to your `scripts.yaml` to orchestrate them in perfect push/pull synchronization:

```yaml
ventoxx_hrv1_mode:
  alias: "Heat Recovery Ventilation - Speed 1 - START"
  sequence:
    # Step 1: Set initial opposite airflow directions to prevent pressure imbalance
    - parallel:
        - service: fan.set_direction
          target: { entity_id: fan.ventoxx_kitchen }
          data: { direction: "reverse" } # Exhaust
        - service: fan.set_direction
          target: { entity_id: fan.ventoxx_living_room }
          data: { direction: "forward" } # Intake
    # Step 2: Turn on and engage the 70-second HRV oscillation timer
    - parallel:
        - service: fan.turn_on
          target: { entity_id: fan.ventoxx_kitchen }
          data: { preset_mode: "Heat Recovery", percentage: 33 }
        - service: fan.turn_on
          target: { entity_id: fan.ventoxx_living_room }
          data: { preset_mode: "Heat Recovery", percentage: 33 }

ventoxx_cooking_mode:
  alias: "Kitchen Cooking - Exhaust - START"
  sequence:
    - parallel:
        # Living Room: High-speed Intake to feed fresh air
        - service: fan.turn_on
          target: { entity_id: fan.ventoxx_living_room }
          data: { preset_mode: "Normal", percentage: 100 }
        - service: fan.set_direction
          target: { entity_id: fan.ventoxx_living_room }
          data: { direction: "forward" }
        # Kitchen: Medium-speed Exhaust to vent odors
        - service: fan.turn_on
          target: { entity_id: fan.ventoxx_kitchen }
          data: { preset_mode: "Normal", percentage: 66 }
        - service: fan.set_direction
          target: { entity_id: fan.ventoxx_kitchen }
          data: { direction: "reverse" }

## Example Dashboard Card
This custom dashboard uses the automatically generated mode sensors to display what the system is doing, alongside buttons to trigger the custom scripts you built above.

Add a Manual Card to your dashboard and paste this YAML:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Ventoxx Master Control
    entities:
      - entity: sensor.ventoxx_living_mode
        name: Living Room Status
      - entity: sensor.ventoxx_kitchen_mode
        name: Kitchen Status
    show_header_toggle: false
    state_color: true

  - type: horizontal-stack
    cards:
      - type: button
        name: HRV Speed 1
        show_name: false
        icon: mdi:fan-speed-1
        tap_action:
          action: call-service
          service: script.ventoxx_hrv1_mode
        icon_height: 50px
      - type: button
        name: Cooking Exhaust
        show_name: false
        icon: mdi:pot-steam-outline
        tap_action:
          action: call-service
          service: script.ventoxx_cooking_mode
        icon_height: 50px
      - type: button
        name: Stop All
        show_name: false
        icon: mdi:stop-circle-outline
        tap_action:
          action: call-service
          service: script.ventoxx_stop
        icon_height: 50px

***

### Why this is a much better README:
1. **The "NEW UPDATE" Banner:** It lets previous users know that a massive upgrade has happened and it is now entirely native.
2. **Removed the YAML Template Sensors:** We completely deleted Step 1 from your old README. Now users just see the clean, auto-generated features.
3. **Streamlined Scripts:** It shows users how to create the push/pull HRV sync using the brand new native commands.

Whenever you push your code to GitHub tomorrow morning, just edit your `README.md` file to match this, and you will have an incredibly professional open-sou

ventoxx_stop:
  alias: "Both Ventoxx Units - STOP"
  sequence:
    - service: fan.turn_off
      target:
        entity_id:
          - fan.ventoxx_living_room
          - fan.ventoxx_kitchen
