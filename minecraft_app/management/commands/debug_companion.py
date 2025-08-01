# Créez le fichier minecraft_app/management/commands/debug_companion.py

from django.core.management.base import BaseCommand
from minecraft_app.models import StoreItem
from minecraft_app.minecraft_service import give_pet_to_player, give_store_item_to_player

class Command(BaseCommand):
    help = 'Debug les compagnons'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='SoCook', help='Pseudo du joueur')
        parser.add_argument('--item-name', type=str, default='Cheval', help='Nom du compagnon')

    def handle(self, *args, **options):
        username = options['username']
        item_name = options['item_name']
        
        self.stdout.write("="*70)
        self.stdout.write(self.style.SUCCESS("🐾 DEBUG COMPAGNONS"))
        self.stdout.write("="*70)
        self.stdout.write(f"👤 Joueur: {username}")
        self.stdout.write(f"🦄 Compagnon: {item_name}")
        self.stdout.write("-"*70)
        
        # 1. Vérifier l'objet en base
        self.stdout.write("\n1️⃣ Vérification de l'objet en base...")
        try:
            store_item = StoreItem.objects.get(name=item_name)
            self.stdout.write(f"   ✅ Objet trouvé: {store_item.name}")
            self.stdout.write(f"   📋 Catégorie: {store_item.category}")
            self.stdout.write(f"   🔧 pet_permission brut: '{store_item.pet_permission}'")
            self.stdout.write(f"   🎯 get_pet_permission(): '{store_item.get_pet_permission()}'")
            
            if store_item.category != 'companion':
                self.stdout.write(self.style.WARNING(f"   ⚠️ PROBLÈME: Catégorie est '{store_item.category}' au lieu de 'companion'"))
            
            if not store_item.pet_permission:
                self.stdout.write(self.style.ERROR("   ❌ PROBLÈME: pet_permission est vide"))
            
        except StoreItem.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"   ❌ Objet '{item_name}' non trouvé"))
            return
        
        # 2. Test de la fonction give_pet_to_player directement
        self.stdout.write("\n2️⃣ Test direct de give_pet_to_player...")
        pet_permission = store_item.get_pet_permission()
        if pet_permission:
            self.stdout.write(f"   🎯 Permission calculée: {pet_permission}")
            try:
                success = give_pet_to_player(username, pet_permission)
                if success:
                    self.stdout.write(self.style.SUCCESS("   ✅ give_pet_to_player: SUCCÈS"))
                else:
                    self.stdout.write(self.style.ERROR("   ❌ give_pet_to_player: ÉCHEC"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Erreur: {e}"))
        else:
            self.stdout.write(self.style.ERROR("   ❌ Impossible de calculer la permission"))
        
        # 3. Test de la fonction give_store_item_to_player
        self.stdout.write("\n3️⃣ Test de give_store_item_to_player...")
        try:
            success = give_store_item_to_player(username, item_name, 1, store_item)
            if success:
                self.stdout.write(self.style.SUCCESS("   ✅ give_store_item_to_player: SUCCÈS"))
            else:
                self.stdout.write(self.style.ERROR("   ❌ give_store_item_to_player: ÉCHEC"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Erreur: {e}"))
        
        # 4. Recommandations
        self.stdout.write("\n" + "="*70)
        self.stdout.write("💡 RECOMMANDATIONS")
        self.stdout.write("="*70)
        
        if store_item.category != 'companion':
            self.stdout.write("🔧 1. Changez la catégorie de l'objet en 'companion' dans l'admin Django")
        
        if not store_item.pet_permission:
            self.stdout.write("🔧 2. Définissez pet_permission dans l'admin Django (ex: 'cheval')")
        
        self.stdout.write("🔧 3. Vérifiez les logs Django pour plus de détails")
        self.stdout.write("🔧 4. Testez en jeu si les messages apparaissent")
        
        self.stdout.write("\n📝 CONFIGURATION RECOMMANDÉE:")
        self.stdout.write(f"   - Nom: {item_name}")
        self.stdout.write("   - Catégorie: companion")
        self.stdout.write("   - pet_permission: cheval")
        self.stdout.write("   - Permission finale: advancedpets.pet.cheval")
        
        self.stdout.write("\n🎯 La permission sera automatiquement préfixée par 'advancedpets.pet.'")
        self.stdout.write("="*70)