db.runCommand({
    collMod: "usuarios",
    validator: 
    { $jsonSchema: {
      required: [
        'password',
        'mail',
        'nombre',
        'rol',
        'fecha_nacimiento',
        'ultima_conexion'
      ],
      properties: {
        mail: {
          bsonType: 'string'
        },
        parent: {
          bsonType: 'string'
        },
        password: {
          bsonType: 'string'
        },
        id: {
          bsonType: 'objectId'
        },
        fecha_nacimiento: {
          bsonType: 'date'
        },
        ultima_conexion: {
          bsonType: 'date'
        },
        nombre: {
          bsonType: 'string'
        },
        rol: {
          bsonType: 'string',
          'enum': [
            'admin',
            'tecnico',
            'cliente'
          ]
        },
        provincia: {
          bsonType: 'string',
          'enum': [
            'A Coruña',
            'Álava',
            'Albacete',
            'Alicante',
            'Almería',
            'Asturias',
            'Ávila',
            'Badajoz',
            'Baleares',
            'Barcelona',
            'Burgos',
            'Cáceres',
            'Cádiz',
            'Cantabria',
            'Castellón',
            'Ciudad Real',
            'Córdoba',
            'Cuenca',
            'Girona',
            'Granada',
            'Guadalajara',
            'Gipuzkoa',
            'Huelva',
            'Huesca',
            'Jaén',
            'La Rioja',
            'Las Palmas',
            'León',
            'Lérida',
            'Lugo',
            'Madrid',
            'Málaga',
            'Murcia',
            'Navarra',
            'Ourense',
            'Palencia',
            'Pontevedra',
            'Salamanca',
            'Segovia',
            'Sevilla',
            'Soria',
            'Tarragona',
            'Santa Cruz de Tenerife',
            'Teruel',
            'Toledo',
            'Valencia',
            'Valladolid',
            'Vizcaya',
            'Zamora',
            'Zaragoza',
            'Ceuta',
            'Melilla'
          ]
        },
        sexo: {
          bsonType: 'string',
          'enum': [
            'M',
            'H',
            'A',
            'T'
          ]
        }
      }
    }
  }
})