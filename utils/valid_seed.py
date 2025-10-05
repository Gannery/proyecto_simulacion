def get_valid_seed() -> int:
    """
    Solicita al usuario una semilla válida (solo dígitos, cantidad par de dígitos).
    
    Returns:
        int: Semilla validada
    """
    while True:
        entrada_usuario = input("Ingresa el número semilla: ")
        
        if entrada_usuario.isdigit() and len(entrada_usuario) % 2 == 0:
            return int(entrada_usuario)
        else:
            print("Error: Debes ingresar solo números y que la cantidad de dígitos sea par.")