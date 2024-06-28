function greet(name: string | null) {
    if (name)
        console.log(name.toUpperCase());
    else
        console.log('Hola!');
}

greet(null); // Error: Argument of type 'null' is not assignable to parameter of type 'string'.