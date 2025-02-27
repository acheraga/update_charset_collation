import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table, inspect, text

# Connexion à la base de données
engine = create_engine('mysql+pymysql://root:root@localhost/pstage')
metadata = MetaData()
metadata.reflect(bind=engine)
inspector = inspect(engine)
new_collation="utf8mb4_unicode_ci" 
new_charset="utf8mb4"

# 1. Exporter les clés étrangères
def export_foreign_keys():
    foreign_keys = []
    
    for table_name in inspector.get_table_names():
        for fk in inspector.get_foreign_keys(table_name):
            fk_info = {
                'table': table_name,
                'name': fk.get('name'),
                'referred_table': fk.get('referred_table'),
                'constrained_columns': fk.get('constrained_columns'),
                'referred_columns': fk.get('referred_columns'),
                'options': fk.get('options', {})
            }
            foreign_keys.append(fk_info)
    
    return foreign_keys

# 2. Supprimer les clés étrangères
def drop_foreign_keys(foreign_keys):
    with engine.begin() as conn:
        for fk in foreign_keys:
            table_name = fk['table']
            fk_name = fk['name']
            if fk_name:
                sql = f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{fk_name}`"
                conn.execute(text(sql))
                print(f"Suppression de la clé étrangère {fk_name} de la table {table_name}")

# 3. Changer la collation de toutes les tables
def change_collation(new_collation="utf8mb4_unicode_ci", new_charset="utf8mb4"):
    with engine.begin() as conn:
        # Obtenir le nom de la base de données
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        
        # Changer la collation de la base de données
        conn.execute(text(f"ALTER DATABASE `{db_name}` CHARACTER SET {new_charset} COLLATE {new_collation}"))
        
        # Obtenir toutes les tables
        tables = inspector.get_table_names()
        
        for table_name in tables:
            # Changer la collation de la table
            conn.execute(text(f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET {new_charset} COLLATE {new_collation}"))
            print(f"Collation de la table {table_name} changée en {new_collation}")

# 4. Restaurer les clés étrangères
def restore_foreign_keys(foreign_keys):
    with engine.begin() as conn:
        for fk in foreign_keys:
            table_name = fk['table']
            referred_table = fk['referred_table']
            constrained_cols = ', '.join([f"`{col}`" for col in fk['constrained_columns']])
            referred_cols = ', '.join([f"`{col}`" for col in fk['referred_columns']])
            
            # Construire les options (ON DELETE, ON UPDATE)
            options = ""
            if 'ondelete' in fk['options']:
                options += f" ON DELETE {fk['options']['ondelete']}"
            if 'onupdate' in fk['options']:
                options += f" ON UPDATE {fk['options']['onupdate']}"
            
            sql = f"""ALTER TABLE `{table_name}` 
                      ADD CONSTRAINT `{fk['name']}` FOREIGN KEY ({constrained_cols}) 
                      REFERENCES `{referred_table}` ({referred_cols}){options}"""
            
            conn.execute(text(sql))
            print(f"Restauration de la clé étrangère {fk['name']} sur la table {table_name}")

# Exécution des fonctions
if __name__ == "__main__":
    # Sauvegarde des clés étrangères
    print("Exportation des clés étrangères...")
    fks = export_foreign_keys()
    
    # Suppression des clés étrangères
    print("Suppression des clés étrangères...")
    drop_foreign_keys(fks)
    
    # Changement de la collation
    print("Changement de la collation des tables...")
    change_collation(new_collation, new_charset)
    
    # Restauration des clés étrangères
    print("Restauration des clés étrangères...")
    restore_foreign_keys(fks)
    
    print("Opération terminée avec succès!")
