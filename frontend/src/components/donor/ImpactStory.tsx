import "./ImpactStory.css";

interface ImpactStoryProps {
  story: string;
  heading?: string;
}

export default function ImpactStory({
  story,
  heading = "Impact Story",
}: ImpactStoryProps) {
  return (
    <section className="impact-story" data-testid="impact-story">
      <h2 className="impact-story__heading">{heading}</h2>
      <p className="impact-story__text">{story}</p>
    </section>
  );
}
