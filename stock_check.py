import uuid
from xml.dom import minidom
from fcb2b_client import load_client_from_yaml



stock_check_path = "/danciko/bwl/dancik-b2b/fcb2b/StockCheck"

def pretty_xml(xml_text: str) -> str:
    try:
        return minidom.parseString(xml_text.encode("utf-8")).toprettyxml(indent="  ")
    except Exception:
        return xml_text



def main():

    client, paths = load_client_from_yaml()
    stock_check_path = paths["stockcheck"]

    #print config details
    while True:
        sku = input("Enter SupplierItemSKU for stock check (blank to exit): ").strip()
        if not sku:
            break

        sku = sku.upper()

        params = {
            "GlobalIdentifier": str(uuid.uuid4()),
            "SupplierItemSKU": sku,
            "TimeStamp": client.get_TimeStamp()
        }

        result = client.get(stock_check_path, params)
        print("\nRequest URL:", result["url"])
        print("\nHTTP Status:", result["status"])
        print("--- XML Response ---")
        print(pretty_xml(result["text"]))
        print("---------------------------")

if __name__ == "__main__":
    main()
