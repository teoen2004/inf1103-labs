class Supplier:
    
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # ----------------------------------------------------- read-only access
    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    # ------------------------------------------------------------- display
    def display_information(self) -> None:
        print("Supplier Information")
        print("-" * 48)
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Name: {self.__name}")
        print(f"Email: {self.__contact_email}")
        print("-" * 48)

    def __str__(self) -> str:
        """One-line summary, handy when a Product shows who supplies it."""
        return (f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
                f"Email: {self.__contact_email}")


