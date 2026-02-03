import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-[10px] text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground [box-shadow:inset_0px_-2px_0px_0px_hsl(209_72%_50%),_0px_1px_6px_0px_hsl(209_72%_63%_/_40%)] hover:bg-primary/90 hover:translate-y-[1px] hover:scale-[0.98] hover:[box-shadow:inset_0px_-1px_0px_0px_hsl(209_72%_50%),_0px_1px_3px_0px_hsl(209_72%_63%_/_30%)] active:translate-y-[2px] active:scale-[0.97] active:[box-shadow:inset_0px_1px_1px_0px_hsl(209_72%_50%),_0px_1px_2px_0px_hsl(209_72%_63%_/_20%)] disabled:shadow-none disabled:hover:translate-y-0 disabled:hover:scale-100",
        secondary:
          "bg-secondary text-secondary-foreground [box-shadow:inset_0px_-2px_0px_0px_hsl(0_0%_12%),_0px_1px_6px_0px_rgba(255,_255,_255,_0.05)] hover:bg-secondary/80 hover:translate-y-[1px] hover:scale-[0.98] hover:[box-shadow:inset_0px_-1px_0px_0px_hsl(0_0%_12%),_0px_1px_3px_0px_rgba(255,_255,_255,_0.03)] active:translate-y-[2px] active:scale-[0.97] active:[box-shadow:inset_0px_1px_1px_0px_hsl(0_0%_12%),_0px_1px_2px_0px_rgba(255,_255,_255,_0.02)] disabled:shadow-none disabled:hover:translate-y-0 disabled:hover:scale-100",
        outline:
          "border border-border bg-transparent text-foreground [box-shadow:inset_0px_-2px_0px_0px_hsl(0_0%_15%),_0px_1px_6px_0px_rgba(255,_255,_255,_0.03)] hover:bg-accent/50 hover:translate-y-[1px] hover:scale-[0.98] hover:[box-shadow:inset_0px_-1px_0px_0px_hsl(0_0%_15%),_0px_1px_3px_0px_rgba(255,_255,_255,_0.02)] active:translate-y-[2px] active:scale-[0.97] active:[box-shadow:inset_0px_1px_1px_0px_hsl(0_0%_15%),_0px_1px_2px_0px_rgba(255,_255,_255,_0.01)] disabled:shadow-none disabled:hover:translate-y-0 disabled:hover:scale-100",
        destructive:
          "bg-destructive text-destructive-foreground [box-shadow:inset_0px_-2px_0px_0px_hsl(0_84%_50%),_0px_1px_6px_0px_hsl(0_84%_60%_/_40%)] hover:bg-destructive/90 hover:translate-y-[1px] hover:scale-[0.98] hover:[box-shadow:inset_0px_-1px_0px_0px_hsl(0_84%_50%),_0px_1px_3px_0px_hsl(0_84%_60%_/_30%)] active:translate-y-[2px] active:scale-[0.97] active:[box-shadow:inset_0px_1px_1px_0px_hsl(0_84%_50%),_0px_1px_2px_0px_hsl(0_84%_60%_/_20%)] disabled:shadow-none disabled:hover:translate-y-0 disabled:hover:scale-100",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3 py-1 text-sm",
        lg: "h-12 px-6 py-3",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />;
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
