import { Star } from 'lucide-react';
import { useState } from 'react';

interface StarRatingProps {
  totalStars?: number;
  initialRating?: number;
  onRatingChange?: (rating: number) => void;
  size?: number;
  readonly?: boolean;
}

export function StarRating({ 
  totalStars = 5, 
  initialRating = 0, 
  onRatingChange,
  size = 32,
  readonly = false
}: StarRatingProps) {
  const [rating, setRating] = useState(initialRating);
  const [hoverRating, setHoverRating] = useState(0);

  const handleClick = (index: number) => {
    if (readonly) return;
    const newRating = index + 1;
    setRating(newRating);
    onRatingChange?.(newRating);
  };

  const handleMouseEnter = (index: number) => {
    if (readonly) return;
    setHoverRating(index + 1);
  };

  const handleMouseLeave = () => {
    if (readonly) return;
    setHoverRating(0);
  };

  return (
    <div className="flex gap-1">
      {Array.from({ length: totalStars }, (_, index) => {
        const isFilled = index < (hoverRating || rating);
        return (
          <button
            key={index}
            type="button"
            onClick={() => handleClick(index)}
            onMouseEnter={() => handleMouseEnter(index)}
            onMouseLeave={handleMouseLeave}
            disabled={readonly}
            className={`transition-all ${readonly ? '' : 'cursor-pointer hover:scale-110'}`}
            aria-label={`Rate ${index + 1} out of ${totalStars}`}
          >
            <Star
              size={size}
              className={`transition-colors ${
                isFilled
                  ? 'fill-yellow-400 stroke-yellow-400'
                  : 'fill-gray-200 stroke-gray-300'
              }`}
            />
          </button>
        );
      })}
    </div>
  );
}
