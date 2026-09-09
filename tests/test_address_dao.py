from daos.address_dao import AddressDao
from models.address import Address


address_dao = AddressDao()

# -------------------------
# TEST CREATE
# -------------------------

address = Address(
    "10 rue Test",
    "Bayonne",
    "64100"
)

id_address = address_dao.create(address)

print("CREATE")
print("ID créé :", id_address)
print(address)


# -------------------------
# TEST READ
# -------------------------

address = address_dao.read(id_address)

print("\nREAD")
print(address)


# -------------------------
# TEST UPDATE
# -------------------------

address = address_dao.read(5)
if address is not None:
    address.street = "12 rue des Fleurs"
    address.city = "Anglet"

    result = address_dao.update(address)

    print("\nUPDATE")
    print("Résultat :", result)
    print(address)


# -------------------------
# TEST DELETE
# -------------------------

address = address_dao.read(6)
if address is not None:
    result = address_dao.delete(address)

    print("\nDELETE")
    print("Résultat :", result)