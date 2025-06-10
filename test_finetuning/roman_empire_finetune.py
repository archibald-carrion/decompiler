#!/usr/bin/env python3
"""
DistilGPT2 Roman Empire Fine-tuning Script
This script demonstrates how to fine-tune DistilGPT2 on Roman Empire content
to create a specialized model for generating Roman history text.
"""

import os
# Suppress oneDNN warning from TensorFlow
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch
from transformers import (
    GPT2LMHeadModel, 
    GPT2Tokenizer, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import argparse
import time
import json
from torch.utils.data import DataLoader

# Set local directory for model storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2-roman-empire")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# Create directories if they don't exist
os.makedirs(BASE_MODEL_DIR, exist_ok=True)
os.makedirs(FINETUNED_MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Roman Empire training data
ROMAN_EMPIRE_TEXTS = [
    "The Roman Empire was one of the largest empires in ancient history. At its peak, it controlled territories spanning from Britain to North Africa and from Spain to the Middle East.",
    
    "Julius Caesar crossed the Rubicon in 49 BCE, marking the beginning of the Roman Civil War. His famous words 'Alea iacta est' meaning 'the die is cast' became legendary.",
    
    "Augustus became the first Roman Emperor in 27 BCE, establishing the Principate and ushering in the Pax Romana, a period of relative peace that lasted for over 200 years.",
    
    "The Roman legions were the backbone of the empire's military might. Each legion consisted of approximately 5,000 heavily armed infantry soldiers organized into cohorts and centuries.",
    
    "The Colosseum in Rome, completed in 80 CE under Emperor Titus, could hold up to 80,000 spectators and hosted gladiatorial contests and public spectacles for over 400 years.",
    
    "Roman engineering marvels included aqueducts that transported fresh water across vast distances, roads that connected the entire empire, and concrete that has lasted for millennia.",
    
    "The fall of the Western Roman Empire in 476 CE marked the end of ancient Rome's dominance, though the Eastern Roman Empire, known as the Byzantine Empire, continued for another thousand years.",
    
    "Marcus Aurelius, the philosopher emperor, ruled from 161 to 180 CE and wrote the Meditations, a series of personal reflections on Stoic philosophy and duty.",
    
    "The Roman Senate, originating in the early Roman Republic, served as an advisory body to the consuls and later to the emperors, representing the aristocratic class of Roman society.",
    
    "Gladiators were trained fighters who battled in amphitheaters throughout the Roman Empire. Most were slaves or prisoners of war, though some free men chose this dangerous profession.",
    
    "The Roman military used advanced tactics including the testudo or tortoise formation, where soldiers would lock their shields together to form a protective shell during sieges.",
    
    "Roman law, codified in the Twelve Tables and later expanded, became the foundation for legal systems throughout Europe and continues to influence modern jurisprudence.",
    
    "The Roman pantheon included gods borrowed from Greek mythology as well as native Roman deities. Jupiter was the king of the gods, while Mars was the god of war.",
    
    "Roman citizenship was highly valued and gradually extended throughout the empire. In 212 CE, Emperor Caracalla granted citizenship to all free inhabitants of the empire.",
    
    "The Roman economy relied heavily on slavery, with slaves working in mines, farms, households, and public works projects throughout the empire.",
    
    "Roman culture spread throughout the Mediterranean world through a process called Romanization, blending local traditions with Roman customs, language, and law.",
    
    "The Praetorian Guard served as the emperor's personal bodyguard and wielded significant political power, sometimes even determining who would become the next emperor.",
    
    "Roman architecture featured innovations like the arch, dome, and concrete construction, exemplified in structures like the Pantheon, which still stands in Rome today.",
    
    "The Roman Empire reached its greatest territorial extent under Emperor Trajan in 117 CE, stretching from Scotland to the Persian Gulf.",
    
    "Roman education emphasized rhetoric, grammar, and philosophy for the wealthy, while common citizens learned practical skills through apprenticeships and trade guilds."
]

def check_requirements():
    """Check if required packages are installed"""
    try:
        import transformers
        print(f"✓ Transformers version: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not installed. Run: pip install transformers")
        return False
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✓ CUDA device: {torch.cuda.get_device_name()}")
    except ImportError:
        print("❌ PyTorch not installed. Run: pip install torch")
        return False
    
    try:
        import datasets
        print(f"✓ Datasets library available")
    except ImportError:
        print("❌ Datasets not installed. Run: pip install datasets")
        return False
    
    return True

def load_base_model():
    """Load base DistilGPT2 model and tokenizer"""
    print(f"Loading base DistilGPT2 model...")
    
    # Check if model exists locally
    if os.path.exists(os.path.join(BASE_MODEL_DIR, "config.json")):
        print("✓ Found existing local model, loading from disk...")
        tokenizer = GPT2Tokenizer.from_pretrained(BASE_MODEL_DIR)
        model = GPT2LMHeadModel.from_pretrained(BASE_MODEL_DIR)
    else:
        print("⬇️  Downloading base model for first time...")
        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        
        # Save to local directory
        print(f"💾 Saving base model to {BASE_MODEL_DIR}")
        tokenizer.save_pretrained(BASE_MODEL_DIR)
        model.save_pretrained(BASE_MODEL_DIR)
        print("✓ Base model saved locally!")
    
    # Set pad token
    tokenizer.pad_token = tokenizer.eos_token
    
    print(f"✓ Base model loaded")
    print(f"✓ Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    return model, tokenizer

def prepare_dataset(tokenizer, max_length=512):
    """Prepare Roman Empire dataset for training"""
    print("📚 Preparing Roman Empire dataset...")
    
    # Tokenize the texts
    def tokenize_function(examples):
        # Add EOS token to each text
        texts = [text + tokenizer.eos_token for text in examples['text']]
        return tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
    
    # Create dataset
    dataset_dict = {"text": ROMAN_EMPIRE_TEXTS}
    dataset = Dataset.from_dict(dataset_dict)
    
    # Tokenize dataset
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names
    )
    
    print(f"✓ Dataset prepared with {len(tokenized_dataset)} examples")
    return tokenized_dataset

def finetune_model(model, tokenizer, dataset, output_dir=FINETUNED_MODEL_DIR, epochs=3):
    """Fine-tune the model on Roman Empire data"""
    print("🏛️  Starting Roman Empire fine-tuning...")
    
    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # GPT-2 is not a masked language model
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        warmup_steps=100,
        prediction_loss_only=True,
        logging_dir=os.path.join(output_dir, "logs"),
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        seed=42,
        fp16=torch.cuda.is_available(),  # Use mixed precision if CUDA available
        dataloader_drop_last=True,
        report_to=None,  # Disable wandb/tensorboard logging
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    
    # Start training
    print(f"🚀 Training for {epochs} epochs...")
    start_time = time.time()
    
    trainer.train()
    
    training_time = time.time() - start_time
    print(f"✓ Training completed in {training_time:.2f} seconds")
    
    # Save the fine-tuned model
    print(f"💾 Saving fine-tuned model to {output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    # Save training info
    training_info = {
        "base_model": "distilgpt2",
        "training_data": "Roman Empire texts",
        "num_examples": len(dataset),
        "epochs": epochs,
        "training_time": training_time,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(os.path.join(output_dir, "training_info.json"), "w") as f:
        json.dump(training_info, f, indent=2)
    
    print("✓ Fine-tuned model saved successfully!")
    return trainer

def load_finetuned_model():
    """Load the fine-tuned Roman Empire model"""
    if not os.path.exists(os.path.join(FINETUNED_MODEL_DIR, "config.json")):
        print("❌ Fine-tuned model not found. Please run training first.")
        return None, None, None
    
    print("Loading fine-tuned Roman Empire model...")
    tokenizer = GPT2Tokenizer.from_pretrained(FINETUNED_MODEL_DIR)
    model = GPT2LMHeadModel.from_pretrained(FINETUNED_MODEL_DIR)
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    print(f"✓ Fine-tuned model loaded on {device}")
    return model, tokenizer, device

def generate_roman_text(model, tokenizer, device, prompt, max_length=200, temperature=0.8, top_p=0.9):
    """Generate Roman Empire themed text"""
    print(f"\n🏛️  Generating Roman Empire text with prompt: '{prompt}'")
    print("-" * 60)
    
    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
    attention_mask = torch.ones_like(inputs)
    
    # Generate text
    start_time = time.time()
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            num_return_sequences=1
        )
    
    generation_time = time.time() - start_time
    
    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"Generated text:\n{generated_text}")
    print(f"\nGeneration time: {generation_time:.2f} seconds")
    print(f"Tokens generated: {len(outputs[0]) - len(inputs[0])}")
    
    return generated_text

def compare_models():
    """Compare base model vs fine-tuned model on Roman Empire prompts"""
    print("\n⚖️  Comparing Base Model vs Fine-tuned Model")
    print("=" * 60)
    
    # Load base model
    print("\nLoading base model...")
    base_model, base_tokenizer = load_base_model()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    base_model.to(device)
    base_model.eval()
    
    # Load fine-tuned model
    print("\nLoading fine-tuned model...")
    ft_model, ft_tokenizer, _ = load_finetuned_model()
    
    if ft_model is None:
        print("Cannot compare - fine-tuned model not available")
        return
    
    # Test prompts
    test_prompts = [
        "The Roman Empire",
        "Julius Caesar",
        "Roman legions were",
        "The Colosseum"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"PROMPT: '{prompt}'")
        print(f"{'='*60}")
        
        print("\n🤖 BASE MODEL:")
        generate_roman_text(base_model, base_tokenizer, device, prompt, max_length=150)
        
        print(f"\n🏛️  FINE-TUNED MODEL:")
        generate_roman_text(ft_model, ft_tokenizer, device, prompt, max_length=150)

def interactive_roman_mode():
    """Interactive mode with fine-tuned Roman Empire model"""
    model, tokenizer, device = load_finetuned_model()
    
    if model is None:
        print("Please train the model first using --train")
        return
    
    print("\n🏛️  Interactive Roman Empire Text Generation")
    print("Enter prompts related to Roman history (type 'quit' to exit)")
    print("-" * 60)
    
    suggested_prompts = [
        "The Roman Emperor",
        "Roman soldiers",
        "In ancient Rome",
        "The gladiators",
        "Roman engineering"
    ]
    
    print("💡 Suggested prompts:", ", ".join(f"'{p}'" for p in suggested_prompts))
    
    while True:
        try:
            prompt = input("\nEnter Roman Empire prompt: ").strip()
            
            if prompt.lower() == 'quit':
                print("Vale! (Farewell!)")
                break
            elif not prompt:
                print("Please enter a prompt or 'quit' to exit")
                continue
            
            generate_roman_text(model, tokenizer, device, prompt)
            
        except KeyboardInterrupt:
            print("\n\nVale! (Farewell!)")
            break
        except Exception as e:
            print(f"Error: {e}")

def show_model_info():
    """Show information about available models"""
    print("\n📊 Model Information")
    print("=" * 40)
    
    # Base model info
    if os.path.exists(BASE_MODEL_DIR):
        base_size = sum(os.path.getsize(os.path.join(BASE_MODEL_DIR, f)) 
                       for f in os.listdir(BASE_MODEL_DIR) 
                       if os.path.isfile(os.path.join(BASE_MODEL_DIR, f)))
        print(f"📁 Base Model: {base_size / (1024*1024):.1f} MB")
    else:
        print("📁 Base Model: Not downloaded")
    
    # Fine-tuned model info
    if os.path.exists(FINETUNED_MODEL_DIR):
        ft_size = sum(os.path.getsize(os.path.join(FINETUNED_MODEL_DIR, f)) 
                     for f in os.listdir(FINETUNED_MODEL_DIR) 
                     if os.path.isfile(os.path.join(FINETUNED_MODEL_DIR, f)))
        print(f"🏛️  Fine-tuned Model: {ft_size / (1024*1024):.1f} MB")
        
        # Show training info if available
        info_file = os.path.join(FINETUNED_MODEL_DIR, "training_info.json")
        if os.path.exists(info_file):
            with open(info_file, 'r') as f:
                training_info = json.load(f)
            print(f"   📚 Training examples: {training_info['num_examples']}")
            print(f"   🔄 Epochs: {training_info['epochs']}")
            print(f"   ⏱️  Training time: {training_info['training_time']:.2f}s")
            print(f"   📅 Trained: {training_info['timestamp']}")
    else:
        print("🏛️  Fine-tuned Model: Not trained yet")

def cleanup_models():
    """Remove all model files"""
    import shutil
    
    removed = []
    if os.path.exists(BASE_MODEL_DIR):
        shutil.rmtree(BASE_MODEL_DIR)
        removed.append("Base model")
    
    if os.path.exists(FINETUNED_MODEL_DIR):
        shutil.rmtree(FINETUNED_MODEL_DIR)
        removed.append("Fine-tuned model")
    
    if removed:
        print(f"✓ Removed: {', '.join(removed)}")
    else:
        print("No models to remove")

def main():
    parser = argparse.ArgumentParser(description='DistilGPT2 Roman Empire Fine-tuning')
    parser.add_argument('--train', action='store_true', help='Fine-tune model on Roman Empire data')
    parser.add_argument('--epochs', type=int, default=3, help='Number of training epochs')
    parser.add_argument('--generate', type=str, help='Generate text with given prompt')
    parser.add_argument('--interactive', action='store_true', help='Interactive generation mode')
    parser.add_argument('--compare', action='store_true', help='Compare base vs fine-tuned models')
    parser.add_argument('--info', action='store_true', help='Show model information')
    parser.add_argument('--cleanup', action='store_true', help='Remove all model files')
    
    args = parser.parse_args()
    
    print("🏛️  DistilGPT2 Roman Empire Fine-tuning")
    print("=" * 50)
    
    # Handle utility commands
    if args.info:
        show_model_info()
        return
    
    if args.cleanup:
        cleanup_models()
        return
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Missing requirements. Please install them and try again.")
        print("Required: pip install transformers torch datasets")
        return
    
    # Training mode
    if args.train:
        try:
            # Load base model
            model, tokenizer = load_base_model()
            
            # Prepare dataset
            dataset = prepare_dataset(tokenizer)
            
            # Fine-tune model
            finetune_model(model, tokenizer, dataset, epochs=args.epochs)
            
            print("\n✅ Fine-tuning completed successfully!")
            print("Use --interactive or --generate to test the fine-tuned model")
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return
    
    # Generation modes
    elif args.generate:
        model, tokenizer, device = load_finetuned_model()
        if model:
            generate_roman_text(model, tokenizer, device, args.generate)
    
    elif args.interactive:
        interactive_roman_mode()
    
    elif args.compare:
        compare_models()
    
    else:
        # Default: show help and model info
        print("\n💡 Usage examples:")
        print("  python script.py --train              # Fine-tune on Roman Empire data")
        print("  python script.py --interactive        # Interactive generation")
        print("  python script.py --generate 'Caesar'  # Generate from prompt")
        print("  python script.py --compare            # Compare models")
        print("  python script.py --info               # Show model info")
        print("\nStart with --train to create the Roman Empire model!")
        show_model_info()

if __name__ == "__main__":
    main()