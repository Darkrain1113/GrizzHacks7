from freewili import FreeWili

# Step 1: Find the first connected FreeWILI device
devices = FreeWili.find_all()
if not devices:
    print("❌ No FreeWILI device found.")
    exit()

device = devices[0]
device.stay_open = True

# Step 2: Send text to the FreeWILI screen
try:
    response = device.show_text_display("Hello, FreeWILI!").expect("Failed to display text")

    if response.is_ok():
        print("✅ Text displayed successfully!")
    else:
        print("⚠️ Text display failed.")

finally:
    device.close()
